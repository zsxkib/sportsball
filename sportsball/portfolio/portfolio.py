"""The portfolio class."""

import os

import numpy as np
import pandas as pd
import quantstats as qs  # type: ignore
from fullmonte import plot, simulate  # type: ignore
from skfolio import RiskMeasure  # type: ignore
from skfolio.optimization import MeanRisk, ObjectiveFunction  # type: ignore

from ..strategy import Strategy


class Portfolio:
    """The portfolio class."""

    def __init__(self, strategies: list[Strategy], name: str) -> None:
        self._name = name
        self._strategies = strategies
        os.makedirs(name, exist_ok=True)

    def fit(self) -> pd.DataFrame:
        """Fits the portfolio to the strategies."""
        # pylint: disable=unsubscriptable-object
        returns = pd.DataFrame([x.returns() for x in self._strategies]).T.fillna(0.0)
        returns.index = pd.to_datetime([i[0] for i in returns.index])

        # Walkforward sharpe optimization
        ret = returns.copy()
        ret[self._name] = np.NaN
        for index in ret.index:
            dt = index.date()
            x = returns[returns.index.date < dt]
            if x.empty:
                ret.loc[index, self._name] = (
                    returns.loc[index] * (1.0 / len(returns.columns.values))
                ).sum()
            else:
                model = MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,
                    objective_function=ObjectiveFunction.MAXIMIZE_RETURN,
                    portfolio_params={"name": "Max Sharpe"},
                )
                model.fit(x.to_numpy())
                ret.loc[index, self._name] = (returns.loc[index] * model.weights_).sum()

        ret = ret.asfreq("D").fillna(0.0)
        ret.index = ret.index.tz_localize("UTC")  # type: ignore
        return ret

    def render(self, returns: pd.Series):
        """Renders the statistics of the portfolio."""
        df = returns.to_frame()
        df["returns"] = df[[returns.name]]
        qs.extend_pandas()
        qs.reports.html(df, "SPY", output=os.path.join(self._name, "test.html"))
        df = simulate(returns)
        plot(df)
