"""RRF excerpt only; does not include retrieval, tenant access or provider calls."""
from __future__ import annotations

from uuid import UUID


def rrf_fuse(*ranked: list[UUID], k: int = 60) -> dict[UUID, float]:
    fused: dict[UUID, float] = {}
    for ranking in ranked:
        for rank, item in enumerate(ranking, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return fused
