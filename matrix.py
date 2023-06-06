import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import os


files=["BEN_pro.csv", "CO_pro.csv", "MXIL_pro.csv", "NO_pro.csv", "NO2_pro.csv", "O3_pro.csv", "PM2.5_pro.csv", "SO2_pro.csv", "TOL_pro.csv"]

#data = pd.DataFrame(columns=["variable", "max", "min", "media", "mediana", "desviacion", "Q1", "Q2", "Q3"])

for f in files:
    varname = f.split("_")
    varname = varname[0]

df = pd.read_csv(f"Database/{f}", sep=";", encoding="utf-8")
df = df.apply(pd.to_numeric, errors="coerce")


#BENCENO
ruta_arquivo = os.path.join("Database", "BEN_pro.csv")
data = pd.read_csv(ruta_arquivo, delimiter=";") 
corr = data.corr()

plt.figure(figsize=(9,9))

ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);

plt.title("Matriz BENCENO")
plt.show()
