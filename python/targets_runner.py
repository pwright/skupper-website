#!/usr/bin/env python3
# targets_runner.py — minimal runner with Plano-style debug logs
from __future__ import annotations

import argparse
import concurrent.futures as cf
import fnmatch
import io
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

# -------------------- Logging (Plano-ish) --------------------

VERBOSE = False
USE_COLOR = False

def _isatty_stderr() -> bool:
    try:
        return sys.stderr.isatty()
    except Exception:
        return False

def _setup_logging(verbose: bool, no_color: bool) -> None:
    global VERBOSE, USE_COLOR
    VERBOSE = bool(verbose or os.environ.get("PLANO_DEBUG") in ("1", "true", "yes"))
    USE_COLOR = False if no_color else _isatty_stderr()

def _c(code: str) -> str:
    return code if USE_COLOR else ""

C_RESET = _c("\x1b[0m")
C_BOLD  = _c("\x1b[1m")
C_DIM   = _c("\x1b[2m")
C_GREEN = _c("\x1b[32m")
C_YELL  = _c("\x1b[33m")
C_RED   = _c("\x1b[31m")
C_BLUE  = _c("\x1b[34m")

def _ts() -> str:
    return time.strftime("%H:%M:%S")

def _log(msg: str) -> None:
    # plain line to stderr
    print(msg, file=sys.stderr)

def log_begin(op: str, detail: str = "") -> float:
    # --> op detail
    if VERBOSE:
        _log(f"{C_BOLD}--> {op}{C_RESET} {detail}".rstrip())
    return time.time()

def log_step(prefix: str, detail: str) -> None:
    # -> or + or ! lines
    if VERBOSE:
        _log(f"{prefix} {detail}")

def log_end(start: float, status: str = "ok") -> None:
    if VERBOSE:
        dur = time.time() - start
        if status == "ok":
            _log(f"{C_GREEN}<-- ok{C_RESET} ({dur:.3f}s)")
        elif status == "warn":
            _log(f"{C_YELL}<-- warn{C_RESET} ({dur:.3f}s)")
        else:
            _log(f"{C_RED}<-- fail{C_RESET} ({dur:.3f}s)")

def log_cmd(cmd: Sequence[str]) -> None:
    if VERBOSE:
        line = " ".join(shlex.quote(c) for c in cmd)
        _log(f"{C_BLUE}+{C_RESET} {line}")

def warn(msg: str) -> None:
    _log(f"{C_YELL}!{C_RESET} {msg}")

def fail(msg: str) -> None:
    _log(f"{C_RED}xx{C_RESET} {msg}")

# -------------------- YAML loading --------------------

def _load_yaml_str(data: str) -> Dict[str, Any]:
    # Prefer Plano helpers if available
    try:
        from plano import yaml as plano_yaml  # type: ignore[attr-defined]
        return plano_yaml.load(data) or {}
    except Exception:
        pass
    try:
        from plano import load_yaml  # type: ignore[attr-defined]
        return load_yaml(io.StringIO(data)) or {}
    except Exception:
        pass
    # Fallback: PyYAML
    try:
        import yaml  # type: ignore
    except Exception:
        fail("No YAML loader found. Install PyYAML or expose plano.load_yaml.")
        raise
    return yaml.safe_load(data) or {}

# -------------------- gitignore support --------------------

def _compile_gitignore(lines: List[str]):
    try:
        import pathspec  # type: ignore
        return pathspec.PathSpec.from_lines("gitwildmatch", lines)
    except Exception:
        pats = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
        return pats  # simple fnmatch fallback

def _gitignore_match(spec, relpath: str) -> bool:
    if spec is None:
        return False
    if hasattr(spec, "match_file"):
        return spec.match_file(relpath)
    return any(fnmatch.fnmatch(relpath, pat) for pat in spec)

# -------------------- Data classes --------------------

@dataclass
class Defaults:
    recursive: bool = True
    follow_symlinks: bool = False
    parallelism: int = 4
    timeout_sec: int = 30
    shell: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)

@dataclass
class ScriptDef:
    name: str
    cmd: str
    args: List[str]
    stdin: Optional[str] = None          # "file" or None
    expects: Optional[str] = None        # "file" or "directory"

@dataclass
class ScriptUse:
    name: str
    timeout_sec: Optional[int] = None

@dataclass
class ExecutionCfg:
    mode: str = "per-file"               # "per-file" or "per-target"
    order: str = "stable"                # "stable" or "filesystem"
    parallelism: Optional[int] = None

@dataclass
class FilterCfg:
    gitignore_paths: List[str] = field(default_factory=list)
    include_globs: List[str] = field(default_factory=lambda: ["**/*"])
    exclude_globs: List[str] = field(default_factory=list)

@dataclass
class Target:
    name: str
    type: str                             # "file" or "directory"
    path: str
    recursive: Optional[bool] = None
    follow_symlinks: Optional[bool] = None
    filter: Optional[FilterCfg] = None
    execution: Optional[ExecutionCfg] = None
    scripts: List[ScriptUse] = field(default_factory=list)

@dataclass
class OutputCfg:
    format: str = "ndjson"               # "text", "json", "ndjson"
    include_fields: List[str] = field(default_factory=lambda: [
        "target", "script", "file", "stdout", "stderr", "exit_code"
    ])
    merge_streams: bool = False

# -------------------- Utils --------------------

def _expand(path: str) -> pathlib.Path:
    return pathlib.Path(os.path.expanduser(path)).resolve()

def _read_file_bytes(p: pathlib.Path) -> bytes:
    with open(p, "rb") as f:
        return f.read()

def _safe_rel(root: pathlib.Path, p: pathlib.Path) -> str:
    try:
        return str(p.relative_to(root))
    except Exception:
        return str(p)

def _build_env(defaults_env: Dict[str, str]) -> Dict[str, str]:
    env = os.environ.copy()
    env.update(defaults_env or {})
    return env

# -------------------- Config builders --------------------

def _load_config_from_path_or_stdin(config_arg: str) -> Dict[str, Any]:
    op = log_begin("load-config", config_arg)
    try:
        if config_arg == "-":
            data = sys.stdin.read()
            if not data:
                raise ValueError("config='-' but no data on stdin")
            cfg = _load_yaml_str(data)
        else:
            p = _expand(config_arg)
            if not p.exists():
                raise FileNotFoundError("Config file not found: {}".format(p))
            cfg = _load_yaml_str(p.read_text(encoding="utf-8"))
        log_end(op, "ok")
        if VERBOSE:
            tgt_count = len(cfg.get("targets") or [])
            _log(f"{C_DIM}.. config targets: {tgt_count}{C_RESET}")
        return cfg
    except Exception:
        log_end(op, "fail")
        raise

def _build_defaults(dct: Dict[str, Any]) -> Defaults:
    dd = dct.get("defaults", {}) or {}
    return Defaults(
        recursive=bool(dd.get("recursive", True)),
        follow_symlinks=bool(dd.get("follow_symlinks", False)),
        parallelism=int(dd.get("parallelism", 4)),
        timeout_sec=int(dd.get("timeout_sec", 30)),
        shell=dd.get("shell"),
        env=dict(dd.get("env", {}) or {}),
    )

def _build_scripts(dct: Dict[str, Any]) -> Dict[str, ScriptDef]:
    res: Dict[str, ScriptDef] = {}
    for name, val in (dct.get("scripts") or {}).items():
        res[name] = ScriptDef(
            name=name,
            cmd=str(val.get("cmd")),
            args=[str(a) for a in (val.get("args") or [])],
            stdin=val.get("stdin"),
            expects=val.get("expects"),
        )
    return res

def _build_filter(fd: Dict[str, Any]) -> FilterCfg:
    return FilterCfg(
        gitignore_paths=[str(_expand(p)) for p in (fd.get("gitignore_paths") or [])],
        include_globs=[str(x) for x in (fd.get("include_globs") or ["**/*"])],
        exclude_globs=[str(x) for x in (fd.get("exclude_globs") or [])],
    )

def _build_execution(ed: Dict[str, Any], defaults: Defaults) -> ExecutionCfg:
    ex = ExecutionCfg()
    if ed is None:
        return ex
    ex.mode = str(ed.get("mode", ex.mode))
    ex.order = str(ed.get("order", ex.order))
    if "parallelism" in ed and ed.get("parallelism") is not None:
        ex.parallelism = int(ed["parallelism"])
    return ex

def _build_targets(dct: Dict[str, Any], defaults: Defaults) -> List[Target]:
    out: List[Target] = []
    for t in (dct.get("targets") or []):
        tg = Target(
            name=str(t["name"]),
            type=str(t["type"]),
            path=str(t["path"]),
            recursive=t.get("recursive"),
            follow_symlinks=t.get("follow_symlinks"),
            # Always pass a dict to _build_filter()
            filter=_build_filter(t.get("filter") or {}),
            execution=_build_execution(t.get("execution"), defaults),
            scripts=[ScriptUse(name=s["use"], timeout_sec=s.get("timeout_sec")) for s in (t.get("scripts") or [])],
        )
        out.append(tg)
    return out

def _build_output(dct: Dict[str, Any]) -> OutputCfg:
    oc = dct.get("output") or {}
    return OutputCfg(
        format=str(oc.get("format", "ndjson")),
        include_fields=[str(x) for x in (oc.get("include_fields") or [
            "target", "script", "file", "stdout", "stderr", "exit_code"
        ])],
        merge_streams=bool(oc.get("merge_streams", False)),
    )

# -------------------- Discovery --------------------

def _collect_matches_for_target(t: Target, defaults: Defaults) -> Tuple[pathlib.Path, List[pathlib.Path]]:
    op = log_begin("discover", f"target={t.name}")
    root = _expand(t.path)

    if t.type == "file":
        if not root.exists():
            log_end(op, "fail")
            raise FileNotFoundError("Target file not found: {}".format(root))
        if VERBOSE:
            _log(f"{C_DIM}.. file: {root}{C_RESET}")
        log_end(op, "ok")
        return root.parent, [root]

    # directory walk
    recursive = defaults.recursive if t.recursive is None else bool(t.recursive)
    follow = defaults.follow_symlinks if t.follow_symlinks is None else bool(t.follow_symlinks)
    filt = t.filter or FilterCfg()

    # .gitignore
    gi_spec = None
    if filt.gitignore_paths:
        lines: List[str] = []
        for p in filt.gitignore_paths:
            try:
                lines.extend(pathlib.Path(p).read_text(encoding="utf-8").splitlines())
            except Exception:
                warn(f"cannot read gitignore: {p}")
        gi_spec = _compile_gitignore(lines)

    includes = filt.include_globs or ["**/*"]
    excludes = filt.exclude_globs or []

    matches: List[pathlib.Path] = []
    # NOTE: pathlib doesn't honor follow_symlinks on glob; rglob follows by default for dirs.
    # We skip adding symlinked files explicitly if follow_symlinks=False.
    walker = (root.rglob("*") if recursive else root.glob("*"))

    for p in walker:
        try:
            if not follow and p.is_symlink():
                continue
            rp = _safe_rel(root, p)
            if gi_spec is not None and _gitignore_match(gi_spec, rp):
                continue
            if excludes and any(fnmatch.fnmatch(rp, pat) for pat in excludes):
                continue
            if includes and not any(fnmatch.fnmatch(rp, pat) for pat in includes):
                continue
            matches.append(p)
        except Exception:
            continue

    if VERBOSE:
        _log(f"{C_DIM}.. root={root} recursive={recursive} follow_symlinks={follow}{C_RESET}")
        _log(f"{C_DIM}.. matches={len(matches)}{C_RESET}")
    log_end(op, "ok")
    return root, matches

# -------------------- Execution --------------------

def _run_cmd(
    cmd: Sequence[str],
    *,
    env: Dict[str, str],
    stdin_bytes: Optional[bytes],
    timeout_sec: Optional[int],
    merge_streams: bool,
) -> Tuple[int, bytes, bytes, float]:
    start = time.time()
    log_cmd(cmd)
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if stdin_bytes is not None else None,
            stdout=subprocess.PIPE,
            stderr=(subprocess.STDOUT if merge_streams else subprocess.PIPE),
            env=env,
        )
        out, err = proc.communicate(input=stdin_bytes, timeout=timeout_sec)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        code = 124  # conventional timeout
        warn("timeout expired (killed process)")
    dur = time.time() - start
    if out is None:
        out = b""
    if err is None:
        err = b""
    if VERBOSE:
        status = f"exit={code} dur={dur:.3f}s"
        _log(f"{C_DIM}.. {status}{C_RESET}")
    return code, out, err, dur

def _record(
    output_fmt: str,
    include_fields: List[str],
    item: Dict[str, Any],
) -> Optional[str]:
    if output_fmt == "ndjson":
        filtered = {k: item.get(k) for k in include_fields if k in item}
        return json.dumps(filtered, ensure_ascii=False)
    elif output_fmt == "json":
        filtered = {k: item.get(k) for k in include_fields if k in item}
        return json.dumps(filtered, ensure_ascii=False)
    elif output_fmt == "text":
        if "stdout" in item and item["stdout"]:
            return str(item["stdout"])
        return "[{target}:{script}] exit={exit_code}".format(
            target=item.get("target"), script=item.get("script"), exit_code=item.get("exit_code")
        )
    else:
        filtered = {k: item.get(k) for k in include_fields if k in item}
        return json.dumps(filtered, ensure_ascii=False)

def _build_mapping(
    *,
    target: Target,
    root: pathlib.Path,
    cur_file: Optional[pathlib.Path],
    tmpdir: pathlib.Path,
) -> Dict[str, str]:
    mapping: Dict[str, str] = {
        "path": str(_expand(target.path)),
        "name": target.name,
        "root": str(root),
        "tmpdir": str(tmpdir),
    }
    if cur_file is not None:
        mapping["file"] = str(cur_file)
        mapping["relpath"] = _safe_rel(root, cur_file)
    return mapping

def _exec_pipeline_for_file(
    *,
    target: Target,
    defaults: Defaults,
    scripts_catalog: Dict[str, ScriptDef],
    root: pathlib.Path,
    file_path: Optional[pathlib.Path],  # None for per-target mode
    env: Dict[str, str],
    timeout_override: Optional[int],
    merge_streams: bool,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix="targets-runner-"))
    prev_stdout: Optional[bytes] = None

    op = log_begin("pipeline", f"target={target.name} file={file_path or root}")
    try:
        for use in target.scripts:
            sd = scripts_catalog.get(use.name)
            if sd is None:
                warn(f"unknown script: {use.name}")
                item = {
                    "target": target.name,
                    "script": use.name,
                    "file": str(file_path) if file_path else str(root),
                    "stdout": "",
                    "stderr": f"unknown script: {use.name}",
                    "exit_code": 127,
                    "duration_sec": 0.0,
                }
                results.append(item)
                break

            mapping = _build_mapping(target=target, root=root, cur_file=file_path, tmpdir=tmpdir)
            cmd = [_template(sd.cmd, mapping)] + [_template(a, mapping) for a in (sd.args or [])]

            stdin_bytes: Optional[bytes] = None
            if sd.stdin == "file":
                if prev_stdout is not None:
                    stdin_bytes = prev_stdout
                elif file_path is not None:
                    try:
                        stdin_bytes = _read_file_bytes(file_path)
                    except Exception as e:
                        warn(f"cannot read file for stdin: {file_path}: {e}")
                        stdin_bytes = None

            timeout_sec = use.timeout_sec if use.timeout_sec is not None else defaults.timeout_sec
            log_step("->", f"script={sd.name} expects={sd.expects or '-'} timeout={timeout_sec}s")

            code, out, err, dur = _run_cmd(
                cmd,
                env=env,
                stdin_bytes=stdin_bytes,
                timeout_sec=(timeout_override or timeout_sec),
                merge_streams=merge_streams,
            )

            prev_stdout = out

            item = {
                "target": target.name,
                "script": sd.name,
                "file": (str(file_path) if file_path else (str(_expand(target.path)) if target.type == "directory" else None)),
                "stdout": out.decode("utf-8", errors="replace"),
                "stderr": ("" if merge_streams else err.decode("utf-8", errors="replace")),
                "exit_code": int(code),
                "duration_sec": round(dur, 4),
            }
            results.append(item)

            if code != 0:
                log_step("xx", f"pipeline halted (exit={code})")
                break
    finally:
        # cleanup tmpdir
        try:
            for child in tmpdir.iterdir():
                try:
                    if child.is_dir():
                        for p in child.rglob("*"):
                            try:
                                p.unlink()
                            except Exception:
                                pass
                        child.rmdir()
                    else:
                        child.unlink()
                except Exception:
                    pass
            tmpdir.rmdir()
        except Exception:
            pass
        log_end(op, "ok")

    return results

# -------------------- Main run loop --------------------

def _template(s: str, mapping: Dict[str, str]) -> str:
    def rep(m: re.Match) -> str:
        key = m.group(1)
        return mapping.get(key, m.group(0))
    return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", rep, s)

def _run_targets(
    config: Dict[str, Any],
    *,
    output_fmt: Optional[str],
    include_fields: List[str],
    merge_streams: bool,
    target_name: Optional[str],
    target_regex: Optional[str],
    jobs_override: Optional[int],
    timeout_override: Optional[int],
    dry_run: bool,
) -> Tuple[List[Dict[str, Any]], str, List[str]]:
    defaults = _build_defaults(config)
    scripts_catalog = _build_scripts(config)
    targets = _build_targets(config, defaults)
    output_cfg = _build_output(config)

    fmt = output_fmt or output_cfg.format
    fields = include_fields or output_cfg.include_fields
    merge = merge_streams if merge_streams is not None else output_cfg.merge_streams

    # filter targets
    before = len(targets)
    if target_name:
        targets = [t for t in targets if t.name == target_name]
    elif target_regex:
        rx = re.compile(target_regex)
        targets = [t for t in targets if rx.search(t.name)]
    if VERBOSE and (target_name or target_regex):
        _log(f"{C_DIM}.. target-filter: {before} -> {len(targets)}{C_RESET}")

    all_results: List[Dict[str, Any]] = []
    op_all = log_begin("run", f"targets={len(targets)} fmt={fmt}")

    for tgt in targets:
        log_step("->", f"target {tgt.name} type={tgt.type}")
        root, matches = _collect_matches_for_target(tgt, defaults)
        exec_cfg = tgt.execution or ExecutionCfg()
        mode = exec_cfg.mode or "per-file"
        order = exec_cfg.order or "stable"
        workers = jobs_override or exec_cfg.parallelism or defaults.parallelism
        env = _build_env(defaults.env)

        if tgt.type == "file":
            files = [matches[0]]
        else:
            if mode == "per-file":
                files = [p for p in matches if p.is_file()]
                if order == "stable":
                    files.sort(key=lambda p: str(p))
            else:
                files = []

        if mode == "per-file" and tgt.type == "directory" and not files:
            warn(f"target '{tgt.name}' matched zero files under {root}")
            continue

        if dry_run:
            # Emit planned invocations as synthetic results
            if mode == "per-file":
                for f in files:
                    mapping = _build_mapping(target=tgt, root=root, cur_file=f, tmpdir=pathlib.Path("/tmp"))
                    for use in tgt.scripts:
                        sd = scripts_catalog.get(use.name)
                        if sd is None:
                            all_results.append({
                                "target": tgt.name, "script": use.name, "file": str(f),
                                "stdout": "", "stderr": "unknown script", "exit_code": 127
                            })
                            continue
                        cmd = [_template(sd.cmd, mapping)] + [_template(a, mapping) for a in (sd.args or [])]
                        all_results.append({
                            "target": tgt.name,
                            "script": sd.name,
                            "file": str(f),
                            "stdout": "DRY-RUN " + " ".join(shlex.quote(c) for c in cmd),
                            "stderr": "",
                            "exit_code": 0,
                        })
            else:
                mapping = _build_mapping(target=tgt, root=root, cur_file=None, tmpdir=pathlib.Path("/tmp"))
                for use in tgt.scripts:
                    sd = scripts_catalog.get(use.name)
                    if sd is None:
                        all_results.append({
                            "target": tgt.name, "script": use.name, "file": str(root),
                            "stdout": "", "stderr": "unknown script", "exit_code": 127
                        })
                        continue
                    cmd = [_template(sd.cmd, mapping)] + [_template(a, mapping) for a in (sd.args or [])]
                    all_results.append({
                        "target": tgt.name,
                        "script": sd.name,
                        "file": str(root),
                        "stdout": "DRY-RUN " + " ".join(shlex.quote(c) for c in cmd),
                        "stderr": "",
                        "exit_code": 0,
                    })
            continue

        if mode == "per-file":
            def job(pth: pathlib.Path) -> List[Dict[str, Any]]:
                return _exec_pipeline_for_file(
                    target=tgt,
                    defaults=defaults,
                    scripts_catalog=scripts_catalog,
                    root=root,
                    file_path=pth,
                    env=env,
                    timeout_override=timeout_override,
                    merge_streams=merge,
                )
            with cf.ThreadPoolExecutor(max_workers=max(1, int(workers))) as ex:
                futs = [ex.submit(job, f) for f in files]
                for fut in cf.as_completed(futs):
                    all_results.extend(fut.result())
        else:
            all_results.extend(
                _exec_pipeline_for_file(
                    target=tgt,
                    defaults=defaults,
                    scripts_catalog=scripts_catalog,
                    root=root,
                    file_path=None,
                    env=env,
                    timeout_override=timeout_override,
                    merge_streams=merge,
                )
            )

    log_end(op_all, "ok")
    return all_results, fmt, fields

# -------------------- CLI --------------------

def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="targets_runner.py")
    ap.add_argument("--config", required=True, help="Path to targets.yaml or '-' for stdin")
    ap.add_argument("--output", choices=["text", "json", "ndjson"], help="Override output format")
    ap.add_argument("--target", help="Run only the named target")
    ap.add_argument("--target-regex", help="Regex filter for target names")
    ap.add_argument("--jobs", type=int, help="Override parallelism")
    ap.add_argument("--timeout", type=int, help="Override per-invocation timeout seconds")
    ap.add_argument("--merge-streams", action="store_true", help="Merge stdout/stderr from scripts")
    ap.add_argument("--dry-run", action="store_true", help="Print what would run; do not execute")
    ap.add_argument("--list-targets", action="store_true", help="List target names and exit")
    ap.add_argument("--verbose", action="store_true", help="Verbose Plano-style logs to stderr")
    ap.add_argument("--no-color", action="store_true", help="Disable ANSI colors in logs")
    return ap.parse_args(argv)

def main(argv: Sequence[str] = None) -> int:
    ns = _parse_args(sys.argv[1:] if argv is None else argv)
    _setup_logging(ns.verbose, ns.no_color)

    try:
        cfg = _load_config_from_path_or_stdin(ns.config)
    except Exception as e:
        fail(f"failed to load config: {e}")
        return 2

    if ns.list_targets:
        try:
            for t in (cfg.get("targets") or []):
                name = t.get("name")
                if name:
                    print(str(name))
            return 0
        except Exception as e:
            fail(f"failed listing targets: {e}")
            return 2

    try:
        results, fmt, fields = _run_targets(
            cfg,
            output_fmt=ns.output,
            include_fields=[],
            merge_streams=bool(ns.merge_streams),
            target_name=ns.target,
            target_regex=ns.target_regex,
            jobs_override=ns.jobs,
            timeout_override=ns.timeout,
            dry_run=bool(ns.dry_run),
        )
    except Exception as e:
        fail(f"run error: {e}")
        return 2

    # Emit results to stdout (according to selected format)
    if fmt == "ndjson":
        for item in results:
            line = _record(fmt, fields, item)
            if line is not None:
                print(line)
    elif fmt == "json":
        out_list = [{k: it.get(k) for k in fields if k in it} for it in results]
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
    elif fmt == "text":
        for item in results:
            line = _record(fmt, fields, item)
            if line is not None:
                print(line)
    else:
        for item in results:
            line = _record("ndjson", fields, item)
            if line is not None:
                print(line)

    # Overall exit code: non-zero if any script failed
    worst = 0
    for it in results:
        ec = int(it.get("exit_code", 0) or 0)
        if ec != 0 and worst == 0:
            worst = ec
    return worst

if __name__ == "__main__":
    sys.exit(main())
