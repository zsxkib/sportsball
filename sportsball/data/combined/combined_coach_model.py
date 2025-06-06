"""Combined coach model."""

from typing import Any

from ..coach_model import CoachModel
from ..field_type import FFILL_KEY
from .null_check import is_null


def create_combined_coach_model(
    coach_models: list[CoachModel],
    identifier: str,
    coach_ffill: dict[str, dict[str, Any]],
) -> CoachModel:
    """Create a coach model by combining many coach models."""
    name = None
    birth_date = None
    age = None
    for coach_model in coach_models:
        coach_model_name = coach_model.name
        if not is_null(coach_model_name):
            name = coach_model_name
        coach_model_birthdate = coach_model.birth_date
        if not is_null(coach_model_birthdate):
            birth_date = coach_model_birthdate
        coach_model_age = coach_model.age
        if not is_null(coach_model_age):
            age = coach_model_age
    if name is None:
        raise ValueError("name is null.")
    coach_model = CoachModel(
        identifier=identifier,
        name=name,
        birth_date=birth_date,
        age=age,
    )

    coach_instance_ffill = coach_ffill.get(identifier, {})
    for field_name, field in coach_model.model_fields.items():
        extra = field.json_schema_extra or {}
        if extra.get(FFILL_KEY, False):  # type: ignore
            current_value = getattr(coach_model, field_name)
            if current_value is None:
                setattr(coach_model, field_name, coach_instance_ffill.get(field_name))
            else:
                coach_instance_ffill[field_name] = current_value
    coach_ffill[identifier] = coach_instance_ffill

    return coach_model
