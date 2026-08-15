# Handoff — Paid Veterinarian Verification Badges and ClickPesa

**Status:** Implemented and verified in the sandbox.

## Scope

VetKonnect now supports a paid public verification badge for active, KYC-verified veterinarian doctor profiles. Badge plans are modeled as weekly, monthly, or yearly configuration records. Prices are deliberately not hard-coded because the commercial amounts were not supplied; administrators must configure the approved TZS prices through Django admin or a controlled data migration before launch.

A professional profile is eligible only when its type is `VETERINARIAN`, `VET_DOCTOR`, or `VETERINARY_DOCTOR`, its KYC status is `VERIFIED`, and the profile is active. Payment success alone never grants the badge. The public profile exposes `is_verified_badge=true` only when an active subscription has a valid start and end time.

## Implemented components

| Component | Implementation |
|---|---|
| Badge plans | `billing.BadgePlan` with weekly, monthly, yearly choices, TZS pricing, duration, and active state |
| Subscriptions | `billing.BadgeSubscription` with pending/active/failed/expired/cancelled/refunded lifecycle and explicit dates |
| Payments | `billing.PaymentTransaction` with client order reference, provider references, amount/currency, channel, status, request/response audit payloads, and failure reason |
| Webhooks | `billing.PaymentWebhookEvent` with provider event idempotency, checksum state, raw event audit, processing status, and error field |
| ClickPesa client | Token generation, one-hour token cache per client instance, USSD-PUSH preview, USSD-PUSH initiation, status query, and timeout-bound requests |
| Integrity | Recursive key-sorted compact JSON HMAC-SHA256 checksum generation and constant-time verification, excluding `checksum` and `checksumMethod` |
| APIs | Public plan listing; authenticated subscription listing; authenticated payment initiation; authenticated payment history; public ClickPesa webhook endpoint |
| Background work | Celery task for USSD-PUSH initiation, status reconciliation, bounded retries, and daily expiry of subscriptions |
| Notifications | In-app notification after successful badge activation through the existing notification/Celery infrastructure |
| Administration | Django admin registration for plans, subscriptions, payments, and webhook events |

## ClickPesa contract used

The implementation uses the official ClickPesa Core API base URL and the documented endpoints for authorization, USSD-PUSH preview, USSD-PUSH initiation, and payment status lookup. Application-level webhook events supported by ClickPesa include `PAYMENT RECEIVED` and `PAYMENT FAILED`. The callback returns HTTP 200 after an accepted or duplicate event. Invalid checksums are rejected when `CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM=1`.

The exact merchant credentials and checksum key are environment-managed through `CLICKPESA_CLIENT_ID`, `CLICKPESA_API_KEY`, and `CLICKPESA_CHECKSUM_KEY`. No credential is stored in a database record, API response, log payload, or source file.

## Subscription and renewal policy

The first payment is initiated through ClickPesa USSD-PUSH using a unique alphanumeric order reference. The badge is activated only after a verified `PAYMENT RECEIVED` webhook with successful status, matching TZS currency, and collected amount at least equal to the configured plan price. Underpayment, currency mismatch, invalid signatures, unknown order references, and failed events do not activate a subscription.

Renewal is represented as a new payment and subscription transaction. The code does not silently auto-charge users. ClickPesa's USSD-PUSH documentation does not by itself establish a recurring mandate contract, so automatic recurring collection remains disabled until the merchant account and ClickPesa product agreement explicitly support it.

## Verification evidence

The following checks passed after implementation:

```text
python3 manage.py makemigrations billing
python3 manage.py check
pytest -q billing/tests/test_billing.py notifications/tests/test_notifications.py
pytest -q
python3 manage.py spectacular --validate --file /tmp/vetconnect-openapi.yaml
```

The final pytest run passed with **36 tests**. Django system checks passed with no issues. OpenAPI validation completed with **zero errors**; two non-blocking enum-name collision warnings remain from unrelated status choice sets and do not affect schema correctness.

The adversarial billing tests cover unverified KYC denial, invalid checksum rejection, underpayment non-activation, successful activation, public badge state, duplicate webhook replay idempotency, and owner-scoped API behavior.

## Production launch requirements

Before enabling live payments, configure ClickPesa application credentials, checksum key, application-level webhook URLs for both payment success and failure, TLS, allowed hosts, worker and Beat processes, Redis, PostgreSQL/PostGIS, monitoring, and provider timeout/alerting policies. Configure the actual weekly, monthly, and yearly TZS prices only after commercial approval. Run a ClickPesa sandbox or merchant test transaction and verify that webhook signatures, amounts, currency, order references, and reconciliation behavior match the production account.

The current sandbox uses SQLite, in-memory Channels, and environment-configured broker defaults. It does not prove live ClickPesa connectivity, production webhook delivery, PostgreSQL transaction isolation, or Redis worker behavior.

## References

[1]: https://docs.clickpesa.com/home/integration-overview "ClickPesa Integration Overview"
[2]: https://docs.clickpesa.com/home/webhooks "ClickPesa Webhooks"
[3]: https://docs.clickpesa.com/api-reference/authorization/generate-token "ClickPesa Generate Authorization Token"
[4]: https://docs.clickpesa.com/payment-api/mobile-money-payment-api/mobile-money-payment-api-overview "ClickPesa Mobile USSD-PUSH API Overview"
[5]: https://docs.clickpesa.com/api-reference/collection/ussd-push-requests/preview-ussd-push-request "ClickPesa Preview USSD-PUSH Request"
[6]: https://docs.clickpesa.com/api-reference/collection/ussd-push-requests/initiate-ussd-push-request "ClickPesa Initiate USSD-PUSH Request"
[7]: https://docs.clickpesa.com/api-reference/collection/querying-for-payments/querying-for-payments "ClickPesa Query Payment Status"
[8]: https://docs.clickpesa.com/home/checksum "ClickPesa Checksum"
