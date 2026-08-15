# HANDOFF-08 — Messaging, Realtime Channels, and Webhooks

## Result

The messaging phase is complete. Conversations have explicit participant membership. Conversation and message reads are restricted to participants. Message creation uses client-supplied idempotency keys scoped to conversation and sender, so retries return the existing message rather than creating duplicates. Webhook endpoint secrets are hashed at rest and never returned.

The current API foundation supports authenticated HTTP messaging. Channels/ASGI infrastructure exists from the foundation phase; a production deployment still requires a real Redis-backed channel layer and worker/endpoint delivery configuration.

## Verification evidence

| Check | Result |
|---|---|
| Messaging migration | Generated and applied |
| Full test suite | **22 passed** |
| `python manage.py check` | Passed |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| OpenAPI generation/validation | Passed with zero warnings/errors |

## Security evidence

Participant isolation was tested with an unauthorized user receiving 404 for a conversation. Duplicate message submission with the same client key produced one database message and a 200 retry response. Webhook secrets were verified to be stored as hashes and not returned in plaintext.

## Next-phase contract

Prompt 09 must implement community content and moderation with author ownership, publication/moderation states, reports, blocks, and administrator moderation isolation.
