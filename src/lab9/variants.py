"""Agent variants for the CI gate (M4). Each is the Lab 8 swarm with bug switches.

    fixed              always trusts the DB (the fix for FM-03)  -> gate must exit 0
    seeded_regression  ticket_trust + pre_deducted + ignore_denied -> gate must exit 1
Registered into lab8.shapes.SHAPES at run time; no Lab 8 file is edited.
"""
from __future__ import annotations

from lab9.variant_agent import make_shape

VARIANTS = {
    "fixed": frozenset({"no_override"}),
    "seeded_regression": frozenset({"ticket_trust", "pre_deducted", "ignore_denied"}),
}


def register() -> list[str]:
    from lab8.shapes import SHAPES
    for name, bugs in VARIANTS.items():
        SHAPES.setdefault(name, make_shape(name, bugs))
    return list(VARIANTS)
