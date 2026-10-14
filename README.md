# pg-lock-witness

Explain captured pg_blocking_pids edges with cycle witnesses, upstream waiters, terminal observed blockers, missing rows and PID-zero prepared-transaction waiters.

Built for postgresql incident responders sharing a captured blocking snapshot. A long blocker list obscures a cycle, upstream waiters and prepared transactions.

## Quickstart

Python 3.10+; no runtime dependencies. The build uses setuptools from the official Python registry. This repository is the install source; no external registry release is claimed.

```sh
git clone https://github.com/nripankadas07/pg-lock-witness.git
cd pg-lock-witness
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/pg-lock-witness example.json
```

On Windows, use `.venv\Scripts\python` and `.venv\Scripts\pg-lock-witness`. Windows behavior has not been exercised; Linux CI is configured to verify Python 3.10, 3.12 and 3.14. An input filename or `-` for standard input is required. Valid analysis returns exit 0, including negative findings; malformed or unsupported input returns exit 2 and a JSON error on stderr. Input is bounded to 1 MiB; duplicate JSON keys and nonfinite numbers fail.

The runnable [example](example.json) uses synthetic data. Run `python pg_lock_witness.py example.json` directly for a source-only demo. Import `analyze(data)` for the Python API; unsupported input raises an exception. The tool makes no network request or operational write.

## Input and output contract

Top level sessions is an array of objects with exactly pid (unique positive integer) and blocking_pids (array of nonnegative integers). PID zero is only a blocker and denotes a prepared transaction. Duplicate blockers are collapsed. Unknown fields and oversized snapshots fail.

The example's installed behavior is asserted in [test_installed_cli.py](test_installed_cli.py). [Unit cases](test_behavior.py) cover positive decisions and meaningful failure cases. The report records actual captured evidence; absence of a finding does not certify an operational environment.

## Limits

A captured cycle is not a durable live deadlock verdict. PostgreSQL may resolve it before analysis; parallel client-visible PID collapse can produce self edges. No database connection, cancellation, victim selection, query text or hard/soft-lock classification. Only explicit captured edges are used; missing sessions stay unknown. At most 256 sessions and 256 blockers per row.

## Validation and research

Run `python -m unittest -v` and `python -m compileall -q pg_lock_witness.py`. [Validation](VALIDATION.md) records exercised configurations. [Research and candidate brief](RESEARCH.md) compares current alternatives and states the inferred demand. No customer adoption or measured performance advantage is claimed.

## Contributing and support

[Contribution guide](CONTRIBUTING.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [MIT license](LICENSE)

Original implementation developed with AI assistance and reviewed through acceptance tests. No competitor source, branding or prose was copied. Primary specifications informed the explicitly supported semantics.
