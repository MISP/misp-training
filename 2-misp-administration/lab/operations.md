# Recovery and update rehearsal

Use this as a tabletop first, then arrange an isolated operational rehearsal with
the platform owner. These procedures were **not executed as a restore or production
upgrade** for the screenshots. Exact commands depend on the supported deployment.

## Make recovery measurable

| Decision | Evidence to record |
| --- | --- |
| Owner and scope | Instance, deployment, data custodians and escalation contacts |
| Recovery point objective (RPO) | Acceptable data loss and backup cadence |
| Recovery time objective (RTO) | Acceptable outage and measured restoration time |
| Consistent recovery set | Database, attachments/files, required configuration and cryptographic material |
| Protection | Encryption, key access, permissions, retention and separate storage |
| External state | Peer/feed/notification consumers, identity provider, TLS, modules and queued work |
| Acceptance | Data completeness, access matrix, keys, schema and representative operations |

Document how the database and attachments are kept consistent at the backup point.
Preserve required encryption/signing material securely; a database dump alone does
not establish recovery of attachments, protected values or trust. Record application,
container/package/source, dependency and knowledge-base versions with the backup.

Restore to an isolated target with outbound peers, feeds, mail and consumers disabled.
Do not accidentally run old scheduled tasks or replay side effects. Validate login
and delegated access, representative events/attachments, sensitive-data access,
key handling, schema/application compatibility and a bounded background job. Compare
expected data with the source recovery point and measure elapsed recovery time.
Record gaps and repeat after fixing them. A successful backup command or a snapshot
is not the same evidence as a successful complete restore.

## Rehearse the supported update path

1. Read release notes, migration requirements and the actual deployment guide.
   Inventory versions, integrations, job backend and available capacity.
2. Choose a representative test copy, maintenance window, owner and acceptance/
   recovery criteria. Prepare and verify a consistent recovery set.
3. Define quiescing and queue handling. Avoid duplicate schedulers and unintended
   feed, sync or notification execution during the change.
4. Apply the supported container, package or source workflow in the test environment.
   Pin container tags/digests and retain compatible configuration; do not treat
   `git pull`, blanket permissions or cache deletion as universal instructions.
5. Validate version, dependencies, schema, health, representative records/attachments,
   the ordinary-account access matrix, keys, jobs/scheduler and authorised integrations.
   A green diagnostic panel alone does not verify those outcomes.
6. Inspect errors and data changes. Observe for an agreed period and compare with
   acceptance criteria before using the rehearsed workflow in the approved window.
7. If recovery criteria are met, use the rehearsed procedure. A code downgrade can
   be incompatible with an already migrated database: restore a consistent compatible
   set when required. Record decisions, evidence and follow-up ownership.

Knowledge-base refreshes are separate changes: record their revisions, enabled
content, templates and any migration implications too.

## Investigate before retrying

| Symptom | First useful evidence |
| --- | --- |
| Task due, no job | Scheduler/process health, identity and task state |
| Job queued | Relevant queue and worker permissions/process |
| Job failed | Its error, source input and dependency health |
| Job completed but unsuitable result | Saved scope/content/version and consumer expectations |

Preserve relevant errors before clearing histories or restarting services. Check
idempotency and impact before retrying. Use MISP audit/application logs, then the
relevant worker, web/PHP, database, Redis and host/container logs. In the reference
image, Supervisor worker files are `app/tmp/logs/misp-workers.log` and
`misp-workers-errors.log`; inspect actual configuration for other deployments.

Select and review diagnostic excerpts before sharing. For vulnerability reports use
the current [MISP security policy](https://github.com/MISP/MISP/blob/2.5/SECURITY.md)
rather than a public issue containing keys or incident data.
