# Worker & queue — durable MySQL job dispatch (ADR-009)

References: [Hono Starter](https://github.com/Joker666/hono-starter) for process layering, [BullMQ docs](https://docs.bullmq.io/) for queue semantics, [MySQL 8.4 docs](https://dev.mysql.com/doc/refman/8.4/en/) for transactions and `SKIP LOCKED`.

**Conditional capability:** no Redis configuration, connection or worker process is required by Core, basic Media or CMS. An enabled module declaring `requiresJobs` requires Redis/BullMQ and worker, but Operations UI is not required for all custom jobs.

## Durable request and dispatch

1. Hono validates session, permission, module, request schema and idempotency key.
2. Within **one MySQL transaction**, save domain intent and `system_jobs` row in `pending` dispatch state, with validated nonsecret payload and deterministic stable queue ID. Return `202` only after commit.
3. Dispatcher claims due jobs in short MySQL transaction using locking/lease (`FOR UPDATE SKIP LOCKED` where supported); commits before calling Redis.
4. Call BullMQ `queue.add` with stable deterministic ID and bounded retries. Mark dispatched only when accepted, conditional on the same claim/lease. If call succeeds then DB update fails, re-dispatch **can** happen: assume at-least-once.
5. Worker validates job type, owning module and payload; claims work through durable business-state guard and processes idempotently. Persist result/attempt/status. Terminal job never repeats irreversible business side effects.

## Rules

- `dispatch_state` and business `status` are distinct. Keep lease expiry, next retry time, dispatch attempt count and request ID in DB. Reclaim expired claim.
- BullMQ `jobId` dedup is **not permanent** after the original job is removed; unique domain effects and database idempotency constraints remain mandatory.
- Recovery from Redis outage leaves MySQL intent queued and subsystem `degraded`, not lost. Do not make Core API readiness fail solely because an optional Redis service is offline.
- Per-job retry profiles and jitter/backoff. Media derivative can retry; backup retry only if safe and manifest states are checked; **production restore never runs as a BullMQ job and never auto-retries**.
- Worker graceful shutdown, heartbeat, queue namespace per clone, no production queue in tests; Redis persistence configuration and network isolation reviewed.

## Exclude

Direct API→Redis enqueue as the **only** durable record, exactly-once claims, globally mandatory worker/Redis, automatic production restore or secret-bearing job payloads.

## Tests

Redis offline before and after MySQL commit; crash after queue.add but before DB ack; duplicate job replay after BullMQ removal; competing dispatchers; lease expiration; worker shutdown; invalid payload; rollback of business effect; module disable; worker absent in Core-only.
