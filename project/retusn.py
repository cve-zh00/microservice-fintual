import pandas as pd
import numpy as np
import cvxpy as cp
import time
from case_test import generate_case_test
import matplotlib.pyplot as plt
def execute_task(num_stocks: int) -> float:
    generate_case_test(num_stocks)
    inicio = time.perf_counter()

    df = pd.read_csv("retornos_fake.csv").dropna(axis=1, how="all")
    df.columns.values[0] = "fecha"
    retornos = df.drop(columns=["fecha"]).to_numpy()

    mu = np.mean(retornos, axis=0)
    Sigma = np.cov(retornos.T)
    Sigma = (Sigma + Sigma.T) / 2 + 1e-5 * np.eye(len(mu))  # regularización

    w = cp.Variable(len(mu))
    max_risk = 0.015
    max_weight = 0.3
    risk = cp.quad_form(w, Sigma)

    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        w <= max_weight,
        risk <= max_risk**2
    ]

    problem = cp.Problem(cp.Maximize(mu @ w), constraints)
    problem.solve(solver=cp.ECOS)

    fin = time.perf_counter()
    print(f"{num_stocks}: {fin - inicio}")
    return fin - inicio
