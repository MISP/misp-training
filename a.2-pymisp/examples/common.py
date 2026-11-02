"""Shared configuration and explicit response checks, without embedded secrets."""
from dataclasses import dataclass, field
import os
from urllib.parse import urlsplit

from pymisp import PyMISP


class TrainingError(RuntimeError):
    """A response did not establish the expected outcome."""


@dataclass(frozen=True)
class Config:
    url: str
    key: str = field(repr=False)
    verify: bool | str = True

    @classmethod
    def from_env(cls):
        url = os.environ.get("MISP_URL", "")
        parsed = urlsplit(url)
        if (not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment):
            raise ValueError("Set MISP_URL to an instance base URL without credentials, query or fragment.")
        if parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        ):
            raise ValueError("Use HTTPS, or loopback HTTP for a disposable local lab.")
        key = os.environ.get("MISP_API_KEY", "")
        if not key or any(c.isspace() for c in key):
            raise ValueError("Set a nonempty MISP_API_KEY without whitespace.")
        # PyMISP.search uses urljoin: the slash preserves an installation subpath.
        return cls(url.rstrip("/") + "/", key, os.environ.get("REQUESTS_CA_BUNDLE") or True)


def connect(config=None):
    """The constructor makes server requests; use only in live exercises."""
    config = config or Config.from_env()
    return PyMISP(config.url, config.key, ssl=config.verify, timeout=(5, 60),
                  debug=False, tool="MISP-PyMISP-training")


def expect_model(result, model):
    if not isinstance(result, model):
        raise TrainingError(f"Expected {model.__name__}; check the API error or proposal locally.")
    return result


def expect_success(result):
    if (not isinstance(result, dict) or "errors" in result or "error" in result
            or result.get("saved") is False or result.get("success") is False):
        raise TrainingError("The API did not confirm the operation; inspect locally before retrying.")
    return result
