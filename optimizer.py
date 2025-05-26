import numpy as np
import polars as pl
import cvxpy as cp
from io import StringIO
from typing import Union, Dict


class Optimizer:
    def __init__(self, df: pl.DataFrame):
        self.df = df
        self.mu = self._calculate_mu(df)
        self.sigma = self._calculate_sigma(df)
        self.w = cp.Variable(len(self.mu))
        self.obj = cp.Maximize(self.mu @ self.w)
        self.risk = cp.quad_form(self.w, self.sigma)

    def _calculate_mu(self, df: pl.DataFrame) -> np.ndarray:
        numeric_cols = [col for col in df.columns if df.schema[col].is_numeric]
        if not numeric_cols:
            raise ValueError("El DataFrame no contiene columnas numéricas.")
        return np.array(df.select([pl.mean(col) for col in numeric_cols]).row(0))

    def _calculate_sigma(self, df: pl.DataFrame) -> np.ndarray:
        return np.cov(df.to_numpy().T)

    def _create_constraints(self, max_risk: float, max_weight: float) -> list:
        constraints = [
            cp.sum(self.w) == 1,
            self.w >= 0,
            self.w <= max_weight,
            self.risk <= max_risk**2
        ]
        return constraints


    def optimize(self, max_risk: float, max_weight: float) -> Dict[str, Dict]:

        constraints = self._create_constraints(max_risk, max_weight)
        problem = cp.Problem(self.obj, constraints)
        problem.solve(solver=cp.SCS, warm_start=True)

        if self.w.value is None:
            raise RuntimeError("No se pudo encontrar una solución óptima.")

        portfolio = {
            ticker: float(peso)
            for ticker, peso in zip(self.df.columns, self.w.value)
        }

        return {
            "optimal_portfolio": portfolio,
        }


class Portfolio:
    def __init__(self, data: Union[str, bytes]):
        self.df = self._parse_and_clean(data)

    def _parse_and_clean(self, data: Union[str, bytes]) -> pl.DataFrame:
        data = data.decode("utf-8") if isinstance(data, bytes) else data
        df = pl.read_csv(StringIO(data.strip()), try_parse_dates=True)
        return self._clean_dataframe(df)

    def _clean_dataframe(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.drop_nulls()
        if not df.columns:
            raise ValueError("El DataFrame está vacío después de eliminar valores nulos.")

        first_col = df.columns[0]
        if df.schema[first_col] in (pl.Datetime, pl.Date):
            df = df.drop(first_col)

        return df.drop_nulls()

    def optimize(self, max_risk: float, max_weight: float) -> Dict[str, Dict]:
        optimizer = Optimizer(self.df)
        return optimizer.optimize(max_risk, max_weight)
