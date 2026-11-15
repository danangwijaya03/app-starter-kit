## Server Guide v2 Addendum — Core-only and optional runtimes

Server deployment (aaPanel, Nginx, PM2) requires **Next.js Web, Hono API, MySQL**. Redis and BullMQ worker are **optional**; only install/start if active module `requiresJobs=true`. Use `modules.config.ts` hash check, private `.env`, DB user separation, Nginx `/api/*` unchanged path, loopback Node ports and HTTPS cookie tests. Deploy from approved commit after CI; migration checked + approved before PM2 restart.

Independent restic encrypted offsite backups are mandatory for production regardless of Operations module. Test restore in isolated database/storage. Production restore never initiated via dashboard API; operator executes separate recovery CLI with authorization and validation gate.

**Target scripts** may not exist in current Next.js preview. Do not execute instructions against production until scripts and tests are implemented. Never treat this addendum as evidence live server is configured.
