import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')


df = pd.read_csv("stats.csv", delimiter=";")

columns = ["variable", "max", "min", "media", "mediana", "desviacion", "Q1", "Q2", "Q3"]
numeric_columns = ["max", "min", "media", "mediana", "desviacion", "Q1", "Q2", "Q3"]
datos_variables = df[numeric_columns]

corr = datos_variables.corr()

print(corr)

plt.figure(figsize=(8,8))

ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20,220, n=220),
    square=True
)


ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)


# plt.title("Matriz de correlación do {}".format(columns[0]))
plt.title("Matriz de correlación das variables")
plt.show()