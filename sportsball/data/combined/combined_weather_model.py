"""Combined weather model."""

from ..weather_model import WeatherModel


def create_combined_weather_model(
    weather_models: list[WeatherModel],
) -> WeatherModel | None:
    """Create a weather model by combining many weather models."""
    if not weather_models:
        return None
    temperature = None
    relative_humidity = None
    for weather_model in weather_models:
        weather_model_temperature = weather_model.temperature
        if weather_model_temperature is not None:
            temperature = weather_model_temperature
        weather_model_relative_humidity = weather_model.relative_humidity
        if weather_model_relative_humidity is not None:
            relative_humidity = weather_model_relative_humidity
    return WeatherModel(temperature=temperature, relative_humidity=relative_humidity)
