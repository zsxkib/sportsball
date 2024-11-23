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

    def fit(self) -> pd.Series:
        """Fits the portfolio to the strategies."""
        if len(self._strategies) == 1:
            returns_series = self._strategies[0].returns()
            returns_series.index = pd.to_datetime([i[0] for i in returns_series.index])
            return returns_series.rename(self._name).asfreq("D").fillna(0.0)

        # pylint: disable=unsubscriptable-object
        returns = pd.DataFrame([x.returns() for x in self._strategies]).T.fillna(0.0)
        returns.index = pd.to_datetime([i[0] for i in returns.index])

        # Walkforward sharpe optimization
        ret = returns.copy()
        for index in ret.index:
            dt = index.date()
            x = returns[returns.index.date < dt]
            if x.empty:
                ret.loc[index] = returns.loc[index] * (
                    1.0 / len(returns.columns.values)
                )
            else:
                print(x.to_numpy())
                model = MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,
                    objective_function=ObjectiveFunction.MAXIMIZE_RETURN,
                    portfolio_params={"name": "Max Sharpe"},
                )
                model.fit(x.to_numpy())
                ret.loc[index] *= model.weights_

        series = pd.Series(
            index=ret.index, data=np.sum(ret.to_numpy(), axis=1), name=self._name
        )
        return series.asfreq("D").fillna(0.0)

    def render(self, returns: pd.Series):
        """Renders the statistics of the portfolio."""
        qs.extend_pandas()
        qs.reports.html(returns, "SPY")
        df = simulate(returns)
        plot(df)
