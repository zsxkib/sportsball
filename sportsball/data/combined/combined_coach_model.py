"""Combined coach model."""

from ..coach_model import CoachModel
from .null_check import is_null


def create_combined_coach_model(
    coach_models: list[CoachModel], identifier: str
) -> CoachModel:
    """Create a coach model by combining many coach models."""
    name = None
    for coach_model in coach_models:
        coach_model_name = coach_model.name
        if not is_null(coach_model_name):
            name = coach_model_name
    if name is None:
        raise ValueError("name is null.")
    return CoachModel(
        identifier=identifier,
        name=name,
    )
