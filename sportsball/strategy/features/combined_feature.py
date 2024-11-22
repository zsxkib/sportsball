"""A feature extractor combining many sub feature extractors."""

import pandas as pd

from .datetime_feature import DatetimeFeature
from .feature import Feature
from .ordinal_feature import OrdinalFeature
from .skill_feature import SkillFeature


class CombinedFeature(Feature):
    """Combined feature extractor class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, features: list[Feature] | None = None) -> None:
        super().__init__()
        if features is None:
            features = [
                SkillFeature(year_slices=[None, 1, 2, 4, 8, 16, 32]),
                DatetimeFeature(),
                OrdinalFeature(),
            ]
        self._features = features

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        for feature in self._features:
            df = feature.process(df)
        return df
