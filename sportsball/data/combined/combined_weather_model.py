"""Combined weather model."""

from ..weather_model import WeatherModel


def create_combined_weather_model(
    weather_models: list[WeatherModel],
) -> WeatherModel | None:
    """Create a weather model by combining many weather models."""
    if not weather_models:
        return None
    temperature = None
    for weather_model in weather_models:
        weather_model_temperature = weather_model.temperature
        if weather_model_temperature is not None:
            temperature = weather_model_temperature
    return WeatherModel(temperature=temperature)
