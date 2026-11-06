"""Pure, offline network policy evaluator prototype.

No network interception, DNS configuration or Gecko integration is performed.
Rules match exact normalized DNS hostnames only, never suffixes or URLs.
"""
from dataclasses import dataclass
from enum import Enum
import ipaddress


class Action(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str


def normalize_host(host: str) -> str:
    if not isinstance(host, str):
        raise TypeError("host must be a string")
    host = host.strip().rstrip(".")
    if not host or any(ch in host for ch in "/\\:@?#%") or any(ch.isspace() for ch in host):
        raise ValueError("expected a DNS hostname, not a URL or address")
    try:
        ascii_host = host.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("invalid DNS hostname") from exc
    if len(ascii_host) > 253 or any(
        not label or len(label) > 63 or label.startswith("-") or label.endswith("-")
        or not all(c.isascii() and (c.isalnum() or c == "-") for c in label)
        for label in ascii_host.split(".")
    ):
        raise ValueError("invalid DNS hostname")
    try:
        ipaddress.ip_address(ascii_host)
    except ValueError:
        return ascii_host
    raise ValueError("IP addresses require a separate policy contract")


@dataclass(frozen=True)
class Policy:
    blocked_hosts: frozenset[str]
    allowed_hosts: frozenset[str] = frozenset()

    @classmethod
    def create(cls, blocked_hosts=(), allowed_hosts=()):
        return cls(
            frozenset(normalize_host(h) for h in blocked_hosts),
            frozenset(normalize_host(h) for h in allowed_hosts),
        )

    def evaluate(self, host: str) -> Decision:
        target = normalize_host(host)
        if target in self.allowed_hosts:
            return Decision(Action.ALLOW, "explicit-exception")
        if target in self.blocked_hosts:
            return Decision(Action.BLOCK, "exact-host-rule")
        return Decision(Action.ALLOW, "no-matching-rule")
