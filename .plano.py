# .plano.py
from __future__ import annotations
import os
import sys
import json
import shlex
import pathlib
import subprocess
from typing import Optional, Sequence
from plano import command  # provided by Plano

# NOTE:
# - Every function in this file is a Plano command (per your constraint).
# - Stdout is reserved for the runner's output; this file logs to stderr.
# - We locate targets_runner.py next to this file or under ./python/.
# - We pass config either by path or via stdin when config == "-".

@command
def run(
    config: str = "targets.yaml",
    output: str = "",                # "", "text", "json", or "ndjson"
    target: str = "",                # exact target name
    target_regex: str = "",          # regex (ignored if target is set)
    jobs: int = 0,                   # 0 = use config/defaults
    timeout: int = 0,                # 0 = use config/defaults
    merge_streams: bool = False,     # default: keep streams separate
) -> None:
    """
    Execute targets from a YAML config file or stdin ("-"), delegating to targets_runner.py.
    Primary results go to stdout. Diagnostics go to stderr. Exit code is propagated.
    """
    # locate runner
    here = pathlib.Path(__file__).resolve().parent
    candidates = [
        here / "targets_runner.py",
        here / "python" / "targets_runner.py",
        pathlib.Path.cwd() / "targets_runner.py",
        pathlib.Path.cwd() / "python" / "targets_runner.py",
    ]
    runner_path: Optional[pathlib.Path] = next((c for c in candidates if c.is_file()), None)
    if not runner_path:
        print("targets_runner.py not found (expected next to .plano.py or under ./python/)", file=sys.stderr)
        sys.exit(2)

    # build CLI
    cmd: list[str] = [sys.executable, str(runner_path), "--config"]
    stdin_bytes: Optional[bytes] = None
    if config == "-":
        data = sys.stdin.buffer.read()
        if not data:
            print("config='-' but no data on stdin", file=sys.stderr)
            sys.exit(2)
        cmd.append("-")
        stdin_bytes = data
    else:
        cfg_path = pathlib.Path(os.path.expanduser(config)).resolve()
        if not cfg_path.exists():
            print(f"config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(2)
        cmd.append(str(cfg_path))

    if output:
        cmd += ["--output", output]
    if target:
        cmd += ["--target", target]
    elif target_regex:
        cmd += ["--target-regex", target_regex]
    if jobs > 0:
        cmd += ["--jobs", str(jobs)]
    if timeout > 0:
        cmd += ["--timeout", str(timeout)]
    if merge_streams:
        cmd += ["--merge-streams"]

    # log and execute
    print("+ " + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_bytes is not None else None,
        stdout=sys.stdout,  # pass-through
        stderr=sys.stderr,  # pass-through
        env=os.environ.copy(),
    )
    if stdin_bytes is not None:
        assert proc.stdin is not None
        proc.stdin.write(stdin_bytes)
        proc.stdin.close()
    sys.exit(proc.wait())

@command
def dry_run(
    config: str = "targets.yaml",
    target: str = "",
    target_regex: str = "",
    jobs: int = 0,
    timeout: int = 0,
) -> None:
    """
    Print what would run without executing scripts (delegates --dry-run to runner).
    """
    here = pathlib.Path(__file__).resolve().parent
    candidates = [
        here / "targets_runner.py",
        here / "python" / "targets_runner.py",
        pathlib.Path.cwd() / "targets_runner.py",
        pathlib.Path.cwd() / "python" / "targets_runner.py",
    ]
    runner_path: Optional[pathlib.Path] = next((c for c in candidates if c.is_file()), None)
    if not runner_path:
        print("targets_runner.py not found (expected next to .plano.py or under ./python/)", file=sys.stderr)
        sys.exit(2)

    cmd: list[str] = [sys.executable, str(runner_path), "--config"]
    stdin_bytes: Optional[bytes] = None
    if config == "-":
        data = sys.stdin.buffer.read()
        if not data:
            print("config='-' but no data on stdin", file=sys.stderr)
            sys.exit(2)
        cmd.append("-")
        stdin_bytes = data
    else:
        cfg_path = pathlib.Path(os.path.expanduser(config)).resolve()
        if not cfg_path.exists():
            print(f"config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(2)
        cmd.append(str(cfg_path))

    if target:
        cmd += ["--target", target]
    elif target_regex:
        cmd += ["--target-regex", target_regex]
    if jobs > 0:
        cmd += ["--jobs", str(jobs)]
    if timeout > 0:
        cmd += ["--timeout", str(timeout)]
    cmd += ["--dry-run"]

    print("+ " + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_bytes is not None else None,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=os.environ.copy(),
    )
    if stdin_bytes is not None:
        assert proc.stdin is not None
        proc.stdin.write(stdin_bytes)
        proc.stdin.close()
    sys.exit(proc.wait())

@command
def list_targets(config: str = "targets.yaml") -> None:
    """
    List target names discovered from the config (delegates --list-targets to runner).
    """
    here = pathlib.Path(__file__).resolve().parent
    candidates = [
        here / "targets_runner.py",
        here / "python" / "targets_runner.py",
        pathlib.Path.cwd() / "targets_runner.py",
        pathlib.Path.cwd() / "python" / "targets_runner.py",
    ]
    runner_path: Optional[pathlib.Path] = next((c for c in candidates if c.is_file()), None)
    if not runner_path:
        print("targets_runner.py not found (expected next to .plano.py or under ./python/)", file=sys.stderr)
        sys.exit(2)

    cmd: list[str] = [sys.executable, str(runner_path), "--config"]
    stdin_bytes: Optional[bytes] = None
    if config == "-":
        data = sys.stdin.buffer.read()
        if not data:
            print("config='-' but no data on stdin", file=sys.stderr)
            sys.exit(2)
        cmd.append("-")
        stdin_bytes = data
    else:
        cfg_path = pathlib.Path(os.path.expanduser(config)).resolve()
        if not cfg_path.exists():
            print(f"config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(2)
        cmd.append(str(cfg_path))

    cmd += ["--list-targets"]

    print("+ " + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_bytes is not None else None,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=os.environ.copy(),
    )
    if stdin_bytes is not None:
        assert proc.stdin is not None
        proc.stdin.write(stdin_bytes)
        proc.stdin.close()
    sys.exit(proc.wait())

@command
def self_test() -> None:
    """
    Smoke test: feeds a tiny inline config via stdin to the runner and verifies it runs.
    """
    here = pathlib.Path(__file__).resolve().parent
    candidates = [
        here / "targets_runner.py",
        here / "python" / "targets_runner.py",
        pathlib.Path.cwd() / "targets_runner.py",
        pathlib.Path.cwd() / "python" / "targets_runner.py",
    ]
    runner_path: Optional[pathlib.Path] = next((c for c in candidates if c.is_file()), None)
    if not runner_path:
        print("targets_runner.py not found (expected next to .plano.py or under ./python/)", file=sys.stderr)
        sys.exit(2)

    inline_yaml = b"""\
version: 1
defaults: { recursive: false, parallelism: 2 }
scripts:
  echo_name:
    cmd: "bash"
    args: ["-lc", "echo NAME={name} PATH={path} FILE={file}"]
    stdin: null
    expects: "file"
targets:
  - name: "tiny-file"
    type: "file"
    path: "./.plano.py"
    scripts:
      - use: "echo_name"
output:
  format: "ndjson"
  include_fields: ["target", "script", "file", "stdout", "exit_code"]
"""

    cmd: list[str] = [sys.executable, str(runner_path), "--config", "-"]
    print("+ " + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=os.environ.copy(),
    )
    assert proc.stdin is not None
    proc.stdin.write(inline_yaml)
    proc.stdin.close()
    sys.exit(proc.wait())
