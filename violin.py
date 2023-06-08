import os
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
plt.style.use('ggplot')



df = pd.read_csv("stats.csv", delimiter=";", encoding="utf-8")

columns = ["variable","max","min","media","mediana","desviacion","Q1","Q2","Q3"]
variables = ["BEN", "CO", "MXIL", "NO", "NO2", "O3", "PM2.5", "SO2", "TOL"]

print(df)


def labeler(varname):
     if varname == "BEN":
         label_title = "BENCENO"
     elif varname == "CO":
        label_title = "CO"
     elif varname == "MXIL":
        label_title  = "M-XILENO"
     elif varname == "NO2":
        label_title = "NO2"
     elif varname == "O3":
        label_title = "O3"
     elif varname == "PM2.5":
         label_title = "PM2.5"
     elif varname == "SO2":
         label_title = "SO2"
     elif varname == "TOL":
         label_title = "TOLUENO"
     return label_title





datos = df[columns[1:]]

maximo = datos["max"].max()
minimo = datos["min"].min()
media = datos["media"].mean()
mediana = datos["mediana"].median()
desviacion = datos["desviacion"].std()
q1 = datos["Q1"].quantile(0.25)
q2 = datos["Q2"].quantile(0.5)
q3 = datos["Q3"].quantile(0.75)

datos_normalizados = (datos - media)/desviacion

print(datos_normalizados)



def violins(nome_variable, ruta_arquivo):
    nome_variable = ["BEN", "CO", "MXIL", "NO", "NO2", "O3", "PM2.5", "SO2", "TOL"]

    combined_df = pd.DataFrame()

     
    for variable in ruta_arquivo:
        df = pd.read_csv(variable, delimiter=";", encoding="utf-8")
        if (nome_variable + variable[1:10]) in df.columns:
            combined_df= pd.concat([combined_df, df[nome_variable + variable[1:10]]], axis=1)
         
        
    
    if combined_df.empty:
        print("Está mal")
    else: 
        print(combined_df.to_string)
        
       
    
    #Gráficas de violín

    fig, ax = plt.subplots(figsize=(9, 9))
    fig.subplots_adjust(bottom=-2)
    #sns.set(style="whitegrid")
    #sns.violinplot(data=combined_df, x="variables", y="valores")
    label_title = labeler(varname=nome_variable)
    # plt.xlabel(label_title)
    # plt.ylabel("Valores")
    plt.xticks(rotation=45)
    plt.title(f"Gráfica de violín do {label_title}")


    plt.show()








    


