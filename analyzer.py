import statistics
import numpy as np
import pandas as pd

"""This file get the matching dates between two variables and
the mean values of those matching dates for each variable"""

fileName1 = 'Temperatura_p'
fileName2 = 'Oxigeno disuelto_p'
# fileName3 = 'Pluviometria_p'

# Get the outlying time stamps for each variable
df = pd.read_csv(f'Database/{fileName1}_out.csv', delimiter=';')
outliers_var1 = list(df['timeStamps'])

df = pd.read_csv(f'Database/{fileName2}_out.csv', delimiter=';')
outliers_var2 = list(df['timeStamps'])

# df = pd.read_csv(f'Database/{fileName3}_out.csv', delimiter=';')
# outliers_var3 = list(df['timeStamps'])

# Get the matching dates
result = [i for i in outliers_var1 if i in outliers_var2]
# result = [i for i in outliers_var2 if i in outliers_var3]

df_final = pd.DataFrame(result, columns = ['matches'])

# Get match percentage
print('Match percentage', (len(result))/statistics.mean([len(outliers_var1), len(outliers_var2)]))

def get_meanvalues(filename):
    
    df = pd.read_csv(f'Database/{filename}_pro.csv', delimiter=';')

    mean_values = []
    for i in result:
    
        startDate = i.split(',')[0][2:-1]
        
        week = int(df.loc[df['startDate'] == startDate, 'week'])

        mean = np.mean(df.loc[df['week'] == week, 'value'])

        mean_values.append(mean)
    
    df_final[f'{filename[0:-2]}'] = mean_values

    return df_final

df_final = get_meanvalues(fileName1)
df_final = get_meanvalues(fileName2)
# df_final = get_meanvalues(fileName3)

print(df_final)

