# Candidate brief and comparison — 14 October 2026

**User:** PostgreSQL incident responders sharing a captured blocking snapshot. **Painful task:** A long blocker list obscures a cycle, upstream waiters and prepared transactions.

**Smallest useful capability:** Explain captured pg_blocking_pids edges with cycle witnesses, upstream waiters, terminal observed blockers, missing rows and PID-zero prepared-transaction waiters.

**Acceptance:** the supplied synthetic example must produce the documented installed result; core edge cases and invalid-input paths must pass; a wheel installed outside the checkout must run the CLI and reject malformed input. The public default commit, remote matrix CI and rendered documentation must be verified before LIVE.

**Demand evidence:** inferred from the workflow and relevant accessible documentation/issues, not a verified customer request. **Discovery path:** descriptive repository topics, a runnable example, searchable edge-case documentation and the user's chronological portfolio index. No unsolicited promotion is performed.

**Distinctness:** The existing sqlite-plan-witness concerns query plans and sqlite-rehearsal concerns database changes; neither captures PostgreSQL wait-for relationships. systemd-order-audit concerns static unit ordering, not runtime lock-manager snapshots.

## Current comparables

pgsty/pigsty is the highest-star PostgreSQL-specific comparable found in the postgres monitoring results. Grafana ranks higher in the broad query but is a general dashboard platform; no exhaustive global ranking is claimed. Queries were executed live on GitHub with Sort by Most stars. Search result coverage is bounded to visible first pages, then relevant established repositories; stars inform discovery, not quality or performance.

| Repository | Stars observed | Latest push observed UTC | License metadata | Observation UTC |
| --- | ---: | --- | --- | --- |
| [pgsty/pigsty](https://github.com/pgsty/pigsty) | 5808 | 2026-09-28T01:07:59Z | Apache-2.0 | 2026-10-14T06:09:36.807Z |
| [dalibo/pg_activity](https://github.com/dalibo/pg_activity) | 3051 | 2026-09-21T08:42:30Z | PostgreSQL | 2026-10-14T06:09:37.014Z |
| [rapidloop/pgmetrics](https://github.com/rapidloop/pgmetrics) | 1112 | 2026-09-09T04:29:12Z | Apache-2.0 | 2026-10-14T06:09:35.837Z |

Pigsty operates a complete PostgreSQL platform, pg_activity monitors live sessions, and pgmetrics collects live server metrics. Use those for live visibility; this MVP makes a small captured edge set reviewable without database credentials.

Comparables' current READMEs, installation examples and accessible issues were inspected. Established tools supply broader integration, docs and community support; this project's support consists of reproducible GitHub reports, source tests and explicit bounded semantics. Its clean install has no runtime dependencies, but that alone establishes no time-to-first-result or reliability advantage. Comparator install success and benchmark performance were not measured. License metadata marked NOASSERTION is unresolved metadata, not a permissive-reuse claim. No reuse was needed.

[Primary behavior reference](https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-SESSION). Competitor README blob hashes, exact star query URLs and source observations are retained in the dated profile research receipt. A local success proves our example, not absence of the behavior in a competitor. Negative results and unsupported configurations remain visible; no superiority claim is made.
