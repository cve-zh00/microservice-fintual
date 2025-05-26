import pandas as pd
import numpy as np
from datetime import datetime, timedelta
def generate_case_test(num_stocks):
    
    num_dias = 500  # 1 año bursátil
    precision = 1e-8
    nombre_archivo = "retornos_fake.csv"

    nombres = [f"STOCK_{i:03}" for i in range(1, num_stocks + 1)]

    hoy = datetime.today()
    fechas = [hoy - timedelta(days=i) for i in range(num_dias * 2)] 
    fechas = [f for f in fechas if f.weekday() < 5][:num_dias] 
    fechas = sorted(fechas)

    data = np.random.normal(loc=0.0005, scale=0.015, size=(num_dias, num_stocks))
    data = np.round(data, 16) 

    df = pd.DataFrame(data, columns=nombres)
    df.insert(0, "fecha", [f.strftime("%Y-%m-%d") for f in fechas])
    df.to_csv(nombre_archivo, index=False)
    print(f"Archivo generado: {nombre_archivo}")
