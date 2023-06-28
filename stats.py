import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np

files=["BEN_pro.csv", "CO_pro.csv", "MXIL_pro.csv", "NO_pro.csv", "NO2_pro.csv", "O3_pro.csv", "PM2.5_pro.csv", "SO2_pro.csv", "TOL_pro.csv"]

stats = pd.DataFrame(columns=["variable", "max", "min", "media", "mediana", "desviacion", "Q1", "Q2", "Q3"])

for f in files:
    varname = f.split("_")
    varname = varname[0]

    df = pd.read_csv(f"Database/{f}", sep=";", encoding="utf-8")
    print(df)

    max = df["value"].max()
    print(max)

    min = df["value"].min()
    print(min)

    media = df["value"].mean()
    print(media)

    mediana = df["value"].median()
    print(mediana)

    desviacion = df["value"].std()
    print(desviacion)

    Q1 = np.percentile(df["value"], 25)
    print(Q1)

    Q2 = np.percentile(df["value"], 50)
    print(Q2)

    Q3 = np.percentile(df["value"], 75)
    print(Q3)

    stats.loc[len(stats.index)] = [varname, max, min, media, mediana, desviacion, Q1, Q2, Q3]

print(stats)

stats.to_csv("stats.csv", sep=";", encoding="utf-8", index=False)





