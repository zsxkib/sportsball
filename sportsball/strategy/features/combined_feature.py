"""A feature extractor combining many sub feature extractors."""

import pandas as pd

from ...data.columns import TRAINING_EXCLUDE_COLUMNS_ATTR
from .datetime_feature import DatetimeFeature
from .feature import Feature
from .ordinal_feature import OrdinalFeature
from .skill_feature import SkillFeature


class CombinedFeature(Feature):
    """Combined feature extractor class."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        pretrain_features: list[Feature] | None = None,
        posttrain_features: list[Feature] | None = None,
    ) -> None:
        super().__init__()
        if pretrain_features is None:
            pretrain_features = [
                SkillFeature(year_slices=[1, 2, 4, 8]),
            ]
        if posttrain_features is None:
            posttrain_features = [
                DatetimeFeature(),
                OrdinalFeature(),
            ]
        self._pretrain_features = pretrain_features
        self._posttrain_features = posttrain_features

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        for feature in self._pretrain_features:
            df = feature.process(df)
        df = df[
            list(set(df.columns.values) - set(df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR]))
        ]
        for feature in self._posttrain_features:
            df = feature.process(df)
        return df
