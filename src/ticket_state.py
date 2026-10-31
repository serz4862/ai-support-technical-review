"""Ticket status machine. Illegal transitions raise domain errors."""

from __future__ import annotations

from typing import Final

TICKET_STATUSES: Final[tuple[str, ...]] = (
    "open",
    "assigned",
    "in_progress",
    "escalated",
    "resolved",
    "closed",
)

ALLOWED_TRANSITIONS: Final[dict[str, frozenset[str]]] = {
    "open": frozenset({"assigned", "in_progress", "resolved", "closed"}),
    "assigned": frozenset({"in_progress", "open", "resolved", "closed"}),
    "in_progress": frozenset({"escalated", "resolved", "closed", "assigned"}),
    "escalated": frozenset({"in_progress", "resolved", "closed"}),
    "resolved": frozenset({"closed"}),
    "closed": frozenset(),
}

REVIEWER_ROLES: Final[frozenset[str]] = frozenset({"admin", "knowledge_manager", "manager"})
CREATOR_ROLES: Final[frozenset[str]] = frozenset(
    {"employee", "admin", "knowledge_manager", "manager"}
)


def can_transition(current: str, target: str) -> bool:
    if current == target:
        return True
    return target in ALLOWED_TRANSITIONS.get(current, frozenset())
