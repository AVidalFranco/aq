import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('ggplot')

from scipy.interpolate import interp1d

file_name = 'BEN_TOL.csv'
df = pd.read_csv(f'results/{file_name}', delimiter=',')

# Define figure
fig = plt.figure(figsize=(9,5))
ax = plt.axes()

# Add the data
smoothed = 'Yes'

if smoothed == 'No':
    ax.plot(df.index, df['B'], color='blue', marker='o', label='Benceno')
    ax.plot(df.index, df['T'], color='red', marker='o', label='Tolueno')

elif smoothed == 'Yes':
    xnew = np.linspace(df.index.min(), df.index.max(), num=500, endpoint=True) # The second parameter affects the length of the data when plotted

    var1 = interp1d(list(df.index), list(df['B']), kind='cubic')
    ax.plot(xnew, var1(xnew), color='darkviolet', label='BEN')
    var2 = interp1d(list(df.index), list(df['T']), kind='cubic')
    ax.plot(xnew, var2(xnew), color='red', label='TOL')
    
    # # In the case of the database with three variables
    # var3 = interp1d(list(df.index), list(df['Scaled_turbidity']), kind='cubic')
    # ax.plot(xnew, var3(xnew), color='darkviolet', label='Turbidity')

# Define axes limits, title and labels
ax.set(xlim=(df.index[0]-1, df.index[-1]+1), ylim=(-0.5, max(df[['B', 'T']].max())*1.10),
    title='BEN v. TOL',
    xlabel='Outlier number', ylabel='Scaled mean value')


# Add legend
plt.legend()

plt.show()
