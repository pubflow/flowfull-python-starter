from fastapi import Request

from app.lib.security.client_ip import get_client_ip


def build_request(headers: list[tuple[bytes, bytes]]) -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": headers,
            "client": ("172.18.0.2", 12345),
        }
    )


def test_get_client_ip_uses_first_forwarded_ip() -> None:
    request = build_request([(b"x-forwarded-for", b"203.0.113.7, 172.18.0.2")])

    assert get_client_ip(request) == "203.0.113.7"


def test_get_client_ip_normalizes_forwarded_header() -> None:
    request = build_request([(b"forwarded", b'for="[2001:db8::1]:443";proto=https')])

    assert get_client_ip(request) == "2001:db8::1"
