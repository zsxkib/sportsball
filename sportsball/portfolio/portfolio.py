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
        # pylint: disable=unsubscriptable-object
        returns = pd.DataFrame([x.returns() for x in self._strategies]).fillna(0.0)

        # Walkforward sharpe optimization
        ret = returns.copy()
        for index in ret.index:
            x = returns[returns.index < index]
            if x.empty:
                ret[index] = returns[index] * (1.0 / len(returns.columns.values))
            else:
                model = MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,
                    objective_function=ObjectiveFunction.MAXIMIZE_RETURN,
                    portfolio_params={"name": "Max Sharpe"},
                )
                model.fit(x)
                ret[index] *= model.weights_

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
