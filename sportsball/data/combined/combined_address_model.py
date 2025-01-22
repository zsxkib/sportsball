"""Combined address model."""

from ..address_model import AddressModel
from .combined_weather_model import create_combined_weather_model


def create_combined_address_model(
    address_models: list[AddressModel],
) -> AddressModel | None:
    """Create a address model by combining many address models."""
    if not address_models:
        return None
    latitude = None
    longitude = None
    housenumber = None
    weather_models = []
    for address_model in address_models:
        address_model_latitude = address_model.latitude
        if address_model_latitude is not None:
            latitude = address_model_latitude
        address_model_longitude = address_model.longitude
        if address_model_longitude is not None:
            longitude = address_model_longitude
        address_model_housenumber = address_model.housenumber
        if address_model_housenumber is not None:
            housenumber = address_model_housenumber
        address_model_weather = address_model.weather
        if address_model_weather is not None:
            weather_models.append(address_model_weather)
    return AddressModel(
        city=address_models[0].city,
        state=address_models[0].state,
        zipcode=address_models[0].zipcode,
        latitude=latitude,
        longitude=longitude,
        housenumber=housenumber,
        weather=create_combined_weather_model(weather_models),  # pyright: ignore
        timezone=address_models[0].timezone,
        country=address_models[0].country,
    )
