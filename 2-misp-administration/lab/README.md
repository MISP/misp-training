# Guided administration lab

Use a disposable, operator-managed MISP 2.5 instance. Allow 90–120 minutes including
the slides, or 25 minutes for the two checkpoints with fixtures prepared. Credentials
are supplied separately through the trainer's approved process; none are provided
in this repository. Record the actual application/knowledge versions and timezone.

The [scenario](scenario.json) describes synthetic records without reusable passwords,
keys or hardcoded database IDs. Resolve IDs after creating records. The
[reference-validation record](reference-validation.json) reports the checks actually
performed on 3 November 2026; it is evidence for that lab, not an executable audit.

## Prepare the fixture

1. Start a fresh instance bound to loopback or an isolated training network. Use
   fresh credentials, required dependencies and the supported deployment workflow.
   Inspect existing feeds, peers, notifications, consumers and scheduled tasks before
   allowing learners to act. Do not reuse production data or identities.
2. Load bundled knowledge through the deployment workflow. Enable the `tlp`
   taxonomy and its tags, the `domain-ip` object template and **List of RFC 5735 CIDR
   blocks**. The reference template has UUID
   `43b3b146-77eb-4931-b4cc-b66c60f28734`, version 11; `tlp` is version 10.
   A later bundle can differ: inspect its name, version and actual hit.
3. Create the local host, Training Partner and Outside Training Group organisations.
   Add External Reference Partner with Local organisation unchecked. Generate new
   UUIDs only for genuinely new lab identities. Resolve roles by their permission
   flags, not by assuming numeric IDs or unchanged standard definitions.
4. Create separate host analyst (User), host Org Admin, partner User and outside
   User accounts. Prepare and disable a synthetic retired host User. Keep the
   site-admin operator separate from access-test accounts. Disable event notifications
   for these fixtures; the reference does not configure a mail relay.
5. Create **Training A and B**, active and non-roaming, with only the host and
   Training Partner as members. Do not grant the partner Extend rights. Limit the
   instance list to the local instance with All orgs unchecked. Save and inspect
   the group, including its UUID, membership and instance constraints.
6. Create an unpublished host-owned private event (distribution 0) and an unpublished
   event with distribution 4 plus this group's ID. Each contains one synthetic
   `ip-dst` attribute `203.0.113.42`, `to_ids=false`, inheriting distribution (5).
   Do not publish, enrich externally or send these records to integrations.
7. Prepare an advanced read-only key for the host analyst with a purpose and short
   expiry. Store the secret separately. The reference key expired on 10 November
   2026; choose an appropriate future date for a new lab.
8. Prepare one peer at `https://peer.example.test` and a MISP-format feed at
   `https://feeds.example.test/misp/`. Use a fresh nonfunctional peer key kept private.
   Disable push/pull, sightings, clusters, analyst-data and collection transfer flags.
   Leave feed Enabled and caching off. Check all existing feeds too. These reserved
   names are placeholders, not services to contact; do not run connection tests,
   cache/fetch buttons or external jobs.

The reference uses `SimpleBackgroundJobs`, Redis and Supervisor with healthy workers
including a scheduler. Configure the supported job backend for your deployment.
Do not start a second scheduler or enable a task until its action, execution identity
and impact are understood.

## Checkpoint 1: delegate and verify an audience

1. As site admin, inspect **Administration → List Roles** and the Org Admin role.
   Identify site/organisation administration, event permission level, API, sync and
   sharing-group flags. Discuss what a customised role would change.
2. Add **Practice Partner** as a local organisation with a fresh UUID. Save it and
   inspect the saved identity. Add `delegate@example.test` to that organisation
   with Org Admin scope, using the approved password/identity workflow and no
   notification delivery. Confirm the saved user and organisation; the screenshot
   shows the form before password entry.
3. Inspect the analyst's advanced-key creation form: purpose, expiry, allowed IPs
   and Read only. Capture only before generation; cancel unless a key is needed.
   The screenshot leaves expiry/source fields empty for discussion, whereas the
   separately prepared verification key has a finite expiry. Retain the key only
   in the approved store and rotate/revoke it under the lab plan.
4. Open the sharing-group Organisations tab, review membership and Extend rights,
   then inspect the saved group. Avoid saving accidental changes during inspection.
5. Use separate sessions or API clients with ordinary identities to obtain this
   matrix. A site administrator's successful read is not an audience test.

| Identity | Private event | Group event | Other control |
| --- | --- | --- | --- |
| Host analyst | Allowed | Allowed | Read-only key reads; write rejected |
| Partner User | Denied | Allowed | Outside host organisation |
| Outside User | Not an intended recipient | Denied | Not a group member |
| Host Org Admin | Allowed | Within own scope | Site settings denied |
| Disabled retired user | — | — | API event listing denied |

The reference checked all results described in the slides. Its denied reads returned
404 and denied privileged/write operations returned 403. Error codes can vary by
endpoint and configuration; verify denial and no mutation, not just a particular
status number. The outside user's private-event read and every possible role/object
combination were not individually tested. Event, object and attribute overrides,
exports and external sync need their own validation.

## Checkpoint 2: observe a controlled change

1. Inspect the enabled taxonomy and domain-ip template. In **Warninglists → Search
   in enabled Warninglists**, check `192.0.2.25`; the reference returns
   `192.0.2.0/24: List of RFC 5735 CIDR blocks`. Explain why a hit is a review aid.
2. Inspect the peer and feed without testing/fetching. Confirm all transfer scopes
   and feed caching remain off. Discuss the approval, trust, scope and bounded
   end-to-end test a real connection would require.
3. Record the previous `MISP.default_event_distribution` value. Set it to **Your
   organisation only** through Server Settings (or the supported settings API).
   Check the saved value and the new-event form. Re-read the two existing fixtures:
   their saved distributions must remain 0 and 4. API clients can supply explicit
   scopes; changing a default does not repair existing records.
4. Review selected non-secret Diagnostics and Workers views. Explain the local
   version-retrieval warning, container update path, worker queue and process health.
   Do not export an unreviewed settings dump or use Kill all workers/queue clearing.
5. Locate the existing **Admin / updateTaxonomies** scheduled task. Confirm it reads
   bundled local taxonomy files, the operator identity is appropriate and its normal
   timing is understood. Force it once in the disposable lab. Follow its **Last Job**
   to Jobs and wait for Completed with 100% progress. In the reference this is task 6,
   job 10, with “All taxonomies are up to date already.” Numeric IDs are lab-specific.
   The task's Status can still say Enqueued after its linked job completes: check
   the final job state. Do not force peer, feed or notification tasks.
6. Filter Audit Logs to model **Organisation** and locate the Practice Partner add
   operation. Check actor, time and changed fields. Review only a narrow non-secret
   excerpt; key/password changes and full user/settings logs are out of scope.
7. Complete the [recovery/update tabletop](operations.md). State what has actually
   been validated, what is still untested, owner, monitoring and next review date.

## Clean up

Revoke disposable keys and sessions. Remove only the lab's resources under the
operator's plan; return any reused lab setting to its recorded baseline. Stop the
isolated containers and delete their disposable volumes when the whole lab is
retired. Do not delete production records, clear shared queues or reset every key.
No remote exchange, email delivery, restore or production update was executed in
the reference run.
