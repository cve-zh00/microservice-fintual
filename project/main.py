import pandas as pd
import numpy as np
import cvxpy as cp
import time
from itertools import product
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
# precarga de datos
mu = np.load("precalculado/mu.npy")
Sigma = np.load("precalculado/sigma.npy")
n = len(mu)
w = cp.Variable(n)
risk = cp.quad_form(w, Sigma)
obj = cp.Maximize(mu @ w)
# función de resolución, crea sus propias variables locales
def execute_task(params: tuple[float, float]) -> float:
    max_risk, max_weight = params
    # Variables y expresiones SYMBOLICAS por llamada


    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        w <= max_weight,
        risk <= max_risk**2
    ]
    problem = cp.Problem(obj, constraints)


    problem.solve(solver=cp.SCS, warm_start=True)

    return problem





if __name__ == "__main__":
    # Preparar combinaciones de parámetros
    N_r = 30
    N_w = 15
    risk_vals   = np.linspace(0.01, 0.05, N_r)
    weight_vals = np.linspace(0.05, 0.5,  N_w)
    combinaciones = list(product(risk_vals, weight_vals))
    tiempos = []
    with ProcessPoolExecutor(4) as executor:
        futures = { executor.submit(execute_task, p): p for p in combinaciones }
        for future in as_completed(futures):
            dur = future.result()
            tiempos.append(dur)

    total_time = sum(tiempos) / 10
    print(f"iteraciones ={len(combinaciones)} time={total_time:.4f}s")

#for n in range(100, 501, 100):

    #duracion = execute_task(n)
    #resultados.append((n, duracion))

# Graficar resultados
#df_resultados = pd.DataFrame(resultados, columns=["Número de activos", "Tiempo (s)"])
#plt.figure(figsize=(10, 5))
#plt.plot(df_resultados["Número de activos"], df_resultados["Tiempo (s)"], marker="o")
#plt.title("Tiempo de resolución vs número de activos")
#plt.xlabel("Número de activos")
#plt.ylabel("Tiempo de ejecución (s)")
#plt.grid(True)
#plt.tight_layout()
#plt.show()
