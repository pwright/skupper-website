# targets runner
Runs YAML-defined automation targets: it loads a targets.yaml-style config, builds defaults/scripts/targets/output settings, and filters execution based on CLI options such as --target or --dry-run (python/targets_runner.py:211, python/targets_runner.py:539).
Discovers matching files or directories for each target using include/exclude globs and optional .gitignore support before handing them to the pipeline (python/targets_runner.py:302).
Executes each target’s script pipeline either per file or per target, manages stdin chaining, timeouts, temporary working dirs, parallelism, and records stdout/stderr per run (python/targets_runner.py:434, python/targets_runner.py:639).
Formats the collected results as NDJSON/JSON/text and exits with the first non-zero script status to signal failure back to callers (python/targets_runner.py:400, python/targets_runner.py:726).

