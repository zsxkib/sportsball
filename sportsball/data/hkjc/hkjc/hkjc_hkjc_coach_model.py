"""HKJC HKJC coach model."""

import pytest_is_running

from ....cache import MEMORY
from ...coach_model import CoachModel


def _create_hkjc_hkjc_coach_model(name: str) -> CoachModel:
    return CoachModel(
        identifier=name,
        name=name,
    )


@MEMORY.cache
def _cached_create_hkjc_hkjc_coach_model(
    name: str,
) -> CoachModel:
    return _create_hkjc_hkjc_coach_model(name)


def create_hkjc_hkjc_coach_model(
    name: str,
) -> CoachModel:
    """Create a coach model based off HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_coach_model(name)
    return _create_hkjc_hkjc_coach_model(name)
