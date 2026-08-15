import hashlib
import hmac
import json
from functools import lru_cache
from typing import Any
import requests
from django.conf import settings


class ClickPesaError(Exception):
    pass


def _canonicalize(value):
    if isinstance(value, dict):
        return {key: _canonicalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    return value


def payload_checksum(payload: dict[str, Any], checksum_key: str) -> str:
    clean = {key: value for key, value in payload.items() if key not in {"checksum", "checksumMethod"}}
    serialized = json.dumps(_canonicalize(clean), separators=(",", ":"), ensure_ascii=False)
    return hmac.new(checksum_key.encode("utf-8"), serialized.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_payload_checksum(payload: dict[str, Any], received_checksum: str, checksum_key: str) -> bool:
    if not received_checksum or not checksum_key:
        return False
    expected = payload_checksum(payload, checksum_key)
    return hmac.compare_digest(expected, received_checksum)


class ClickPesaClient:
    def __init__(self):
        self.base_url = settings.CLICKPESA_BASE_URL
        self.timeout = settings.CLICKPESA_TIMEOUT_SECONDS

    def _headers(self, token=None):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = token
        return headers

    @lru_cache(maxsize=1)
    def _token(self):
        if not settings.CLICKPESA_CLIENT_ID or not settings.CLICKPESA_API_KEY:
            raise ClickPesaError("ClickPesa credentials are not configured.")
        response = requests.post(
            f"{self.base_url}/generate-token",
            headers={"client-id": settings.CLICKPESA_CLIENT_ID, "api-key": settings.CLICKPESA_API_KEY, "Accept": "application/json"},
            timeout=self.timeout,
        )
        if not response.ok:
            raise ClickPesaError(f"ClickPesa token request failed with HTTP {response.status_code}.")
        data = response.json()
        token = data.get("token")
        if not token:
            raise ClickPesaError("ClickPesa token response did not include a token.")
        return token

    def _post(self, path, payload):
        body = dict(payload)
        if settings.CLICKPESA_CHECKSUM_KEY:
            body["checksum"] = payload_checksum(body, settings.CLICKPESA_CHECKSUM_KEY)
        response = requests.post(f"{self.base_url}{path}", headers=self._headers(self._token()), json=body, timeout=self.timeout)
        if not response.ok:
            raise ClickPesaError(f"ClickPesa request failed with HTTP {response.status_code}.")
        return response.json()

    def preview_ussd_push(self, *, amount, order_reference, phone_number, currency="TZS"):
        return self._post("/payments/preview-ussd-push-request", {"amount": str(amount), "currency": currency, "orderReference": order_reference, "phoneNumber": phone_number, "fetchSenderDetails": False})

    def initiate_ussd_push(self, *, amount, order_reference, phone_number, currency="TZS"):
        return self._post("/payments/initiate-ussd-push-request", {"amount": str(amount), "currency": currency, "orderReference": order_reference, "phoneNumber": phone_number})

    def payment_status(self, order_reference):
        response = requests.get(f"{self.base_url}/payments/{order_reference}", headers=self._headers(self._token()), timeout=self.timeout)
        if not response.ok:
            raise ClickPesaError(f"ClickPesa status request failed with HTTP {response.status_code}.")
        return response.json()
