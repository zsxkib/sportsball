"""The base class for a data model."""

import pandas as pd
import requests_cache


class Model:
    """The base model class."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        self._session = session

    @property
    def session(self) -> requests_cache.CachedSession:
        """Return the session."""
        return self._session

    def to_frame(self) -> pd.DataFrame:
        """Render the model as a dataframe."""
        raise NotImplementedError("to_frame not implemented by parent class.")
