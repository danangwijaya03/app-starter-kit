# Worker & queues — BullMQ/Redis with Hono API

Sources: https://github.com/Joker666/hono-starter ; https://github.com/taskforcesh/bullmq ; https://docs.bullmq.io/ .

**Adopt:** separate worker Node process, queue naming/prefix isolation, safe retry/backoff, strict job payload schemas, idempotency key and monitoring. API enqueues, worker processes; do not let web import Redis credentials. One queue namespace per cloned project.

**Guardrails:** retries must not duplicate money/role/backup side effects; restore jobs never auto-retry; background job identity/authorization are verified before dispatch. Worker must handle shutdown and recover with durable state.

**Tests:** successful job, invalid payload denied, replay safe, retry limits, worker restart, cancellation/timeout, isolated Redis, no production queue in test.
