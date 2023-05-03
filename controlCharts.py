import os
from statistics import variance
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

"""Implementation of the control charts on the processed data with the Nelson rules:

Rule 1: one point is more than 3 standars deviations from the mean.

Rule 2: Nine (or more) points in a row are on the same side of the mean.

Rule 3: Six (or more) points in a row are continually increasing (or decreasing).

Rule 4: Fourteen (or more) points in a row alternate in direction, increasing then 
decreasing.

Rule 5: Two (or three) out of three points in a row are more than 2 standard deviations 
from the mean in the same direction.

Rule 6: Four (or five) out of five points in a row are more than 1 standard deviation 
from the mean in the same direction.

Rule 7: Fifteen points in a row are all within 1 standard deviation of the mean on 
either side of the mean.

Rule 8: Eight points in a row exist, but none within 1 standard deviation of the mean, 
and the points are in both directions from the mean."""

# Several formatting functions are needed
def format_arr(rule, result):
    
    rule_arr = 'rule_' + str(rule)
    return [index for index,val in enumerate(result[rule_arr]) if val]

def format_arr_fda(data):
    
    return [index for index,val in enumerate(data) if not val]

def plotAxlines(array):
    
    mean = np.mean(array)
    std = np.std(array)
    colors = ['black','green','yellow','red']
    
    for level,color in enumerate(colors):
        upper = mean + std*level
        lower = mean - std*level
        plt.axhline(y=upper, linewidth=1, color=color)
        plt.axhline(y=lower, linewidth=1, color=color)
    
    return

def labeler(varname):

    if varname == 'Amonio':
        label_title = r'$NH_4$ '
        label_y_axis = r' (m*g/L)$'
    elif varname == 'Conductividad' or varname == 'Conductividad_p1' or varname == 'Conductividad_p2' or varname == 'Conductividad_p' or varname == 'Conductividad_val':
        label_title = r'Conductivity '
        label_y_axis = r' (\mu*S/cm)$'
    elif varname == 'Nitratos':
        label_title = r'$NO_{3^-}$ '
        label_y_axis = r' (m*g/L)$'
    elif varname == 'Oxigeno disuelto' or varname == 'Oxigeno disuelto_p' or varname == 'Oxigeno disuelto_p1' or varname == 'Oxigeno disuelto_p2':
        label_title = r'$O_2$ '
        label_y_axis = r' (m*g/L)$'
    elif varname == 'pH' or varname == 'pH_p1' or varname == 'pH_p2' or varname == 'pH_p3' or varname == 'pH_p':
        label_title = r'pH '
        label_y_axis = r' $'
    elif varname == 'Temperatura' or varname == 'Temperatura_p1' or varname == 'Temperatura_p2' or varname == 'Temperatura_p':
        label_title = r'Temperature '
        label_y_axis = u' (\N{DEGREE SIGN}C)$'
    elif varname == 'Temperatura_rio_p' or varname == 'Temperatura_rio_p1' or varname == 'Temperatura_rio_p2':
        label_title = r'River water remperature '
        label_y_axis = r'Temperature ' +u'(\N{DEGREE SIGN}C)'
    elif varname == 'Caudal' or varname == 'Caudal_p' or varname == 'Caudal_p1' or varname == 'Caudal_p2':
        label_title = r'Flow '
        label_y_axis = r' (m^3/s)$'
    elif varname == "Turbidez" or varname == 'Turbidez_p' or varname == 'Turbidez_p1' or varname == 'Turbidez_p2':
        label_title = r'Turbidity '
        label_y_axis = r' (NRU)$'
    elif varname == "Pluviometria" or varname == 'Pluviometria_p1' or varname == 'Pluviometria_p2' or varname == 'Pluviometria_p':
        label_title = r'Pluviometry '
        label_y_axis = r' (mm)$'
    elif varname == "Nivel" or varname == 'Nivel_p1' or varname == 'Nivel_p2' or varname == 'Nivel_p':
        label_title = r'Water level'
        label_y_axis = r'Water level ' + r'(m)'


    return label_title, label_y_axis

# Check which dates are considered outleirs according to the Nelson rules
def validator(rule, dates, result):
    
    outliers = []
    
    for i,j in zip(dates, result[str(rule)]):
        
        if j == 1:
            
            outliers.append(i)

    return outliers

def controlCharts(varname, datamatrix, timestamps, timeframe, vargraph, outleirsresults):
    
    """varGraph (string) contains the type of control chart:
    mean: x bar chart
    stds: s chart
    ranges: mR chart"""
    
    numberGroups = len(datamatrix)
    lenGroups = len(datamatrix[1])
    
    # define list variable for group means
    x = []

    # define list variable for group standard deviations
    s = []

    for group in datamatrix:
        
        x.append((np.mean(group)).round(3))
        s.append((np.std(group)).round(3))
        
        mrs = [[] for i in range(numberGroups)]
        
    # Get and append moving ranges
    counter = 1
    for i,w in zip(datamatrix, range(len(mrs))):
        for j in range(len(i)):
            result = abs(round(i[j] - i[j-1], 2))
            mrs[w].append(result)
            counter += 1
            
            if counter == lenGroups:
                break
    
    # Define list variable for the moving ranges
    mr = []
    for i in mrs:
        mr.append(round(np.mean(i), 4))

    # The historical mean for the process variable in question
    mean_x = (np.mean(x)).round(3)
    mean_s = (np.mean(s)).round(3)
    mean_mr = (np.mean(mr)).round(3)

    # the historical standard deviation for the process variable in question
    std_x = (np.std(x)).round(3)
    std_s = (np.std(s)).round(3)
    std_mr = (np.std(mr)).round(3)

    # Create database with the key information for each graph
    dfchart = pd.DataFrame(list(zip(x, s, mr)), columns=['mean', 'stds', 'ranges'])
    
    # Define the Nelson rules
    class nelson:

        # first nelson rule
        def rule1(self, data, mean, std):
            sigmaUp = mean + 3*std
            sigmaDown = mean -3*std

            def isBetween(value, lower, upper):
                isBetween = value < upper and value > lower
                return 0 if isBetween else 1

            data['rule_1'] = dfchart.apply(lambda row: isBetween(row[vargraph], sigmaDown, sigmaUp), axis=1)

        # second nelson rule
        def rule2(self, data, mean):
            values = [0]*len(dfchart)
            
            # +1 means upside, -1 means downside
            upsideOrDownside = 0
            counter = 0
            for i in range(len(dfchart)):
                
                number = dfchart.iloc[i][vargraph]
                
                if number > mean:
                    if upsideOrDownside == 1:
                        counter += 1
                    else:
                        upsideOrDownside = 1
                        counter = 1
                elif number < mean:
                    if upsideOrDownside == -1:
                        counter += 1
                    else:
                        upsideOrDownside = -1
                        counter = 1
                
                if counter >= 9:
                    values[i] = 1
            
            data['rule_2'] = values
        
        # third nelson rule
        def rule3(self, data):
            
            values = [0]*len(dfchart)
            
            previousNumber = dfchart.iloc[0][vargraph]
            # +1 means increasing, -1 means decreasing
            increasingOrDecreasing = 0
            counter = 0
            for i in range(1, len(dfchart)):
                number = dfchart.iloc[i][vargraph]
                if number > previousNumber:
                    if increasingOrDecreasing == 1:
                        counter += 1
                    else:
                        increasingOrDecreasing = 1
                        counter = 1
                elif number < previousNumber:
                    if increasingOrDecreasing == -1:
                        counter += 1
                    else:
                        increasingOrDecreasing = -1
                        counter = 1
                
                if counter >= 6:
                    values[i] = 1
                    
                previousNumber = number
                    
            data['rule_3'] = values
        
        # fourth nelson rule
        def rule4(self, data):
            values = [0]*len(dfchart)
            
            previousNumber = dfchart.iloc[0][vargraph]
            # +1 means increasing, -1 means decreasing
            bimodal = 0
            counter = 1
            for i in range(1, len(dfchart)):
                number = dfchart.iloc[i][vargraph]
                
                if number > previousNumber:
                    bimodal += 1
                    if abs(bimodal) != 1:
                        counter = 0
                        bimodal = 0
                    else:
                        counter +=1
                elif number < previousNumber:
                    bimodal -= 1
                    if abs(bimodal) != 1:
                        counter = 0
                        bimodal = 0
                    else:
                        counter += 1
                
                previousNumber = number
                
                if counter >= 14:
                    values[i] = 1
            
            data['rule_4'] = values
        
        # fifth nelson rule
        def rule5(self, data, mean, std):
            if len(dfchart) < 3: return
            
            values = [0]*len(dfchart)
            twosigmaUp = mean + 2*std
            twosigmaDown = mean - 2*std
            
            for i in range(len(dfchart) - 3):
                first = dfchart.iloc[i][vargraph]
                second = dfchart.iloc[i+1][vargraph]
                third = dfchart.iloc[i+2][vargraph]
                
                setValue = False
                validCounter = 0
                if first > mean and second > mean and third > mean:
                    validCounter += 1 if first > twosigmaUp else 0
                    validCounter += 1 if second > twosigmaUp else 0
                    validCounter += 1 if third > twosigmaUp else 0
                    setValue = validCounter >= 2
                elif first < mean and second < mean and third < mean:
                    validCounter += 1 if first < twosigmaDown else 0
                    validCounter += 1 if second < twosigmaDown else 0
                    validCounter += 1 if third < twosigmaDown else 0
                    setValue = validCounter >= 2
                
                if setValue:
                    values[i+2] = 1
            
            data['rule_5'] = values
        
        # sixth nelson rule 
        def rule6(self, data, mean, std):
            if len(dfchart) < 5: return
            
            values = [0]*len(dfchart)
            onesigmaUp = mean - std
            onesigmaDown = mean + std
            
            for i in range(len(dfchart) - 5):
                pVals = list(map(lambda x: dfchart.iloc[x][vargraph], range(i, i+5)))
                
                setValue = False # revisar estas condiciones 
                if len(list(filter(lambda x: x > mean, pVals))) == 5:
                    setValue = len(list(filter(lambda x: x > onesigmaDown, pVals))) >= 4
                elif len(list(filter(lambda x: x < mean, pVals))) == 5:
                    setValue = len(list(filter(lambda x: x < onesigmaUp, pVals))) >= 4
                    
                if setValue:
                    values[i+4] = 1
                    
            data['rule_6'] = values
        
        # fifth nelson rule
        def rule7(self, data, mean, std):
            if len(dfchart) < 15: return
            
            values = [0]*len(dfchart)
            onesigmaUp = mean + std
            onesigmaDown = mean - std
            
            for i in range(len(dfchart) - 15):
                setValue = True
                for y in range(15):
                    item = dfchart.iloc[i + y][vargraph]
                    if item >= onesigmaUp or item <= onesigmaDown:
                        setValue = False
                        break
                
                if setValue:
                    values[i+14] = 1
            
            data['rule_7'] = values
        
        # eigth nelson rule
        def rule8(self, data, mean, std):
            if len(dfchart) < 8: return
            
            values = [0]*len(dfchart)
            
            for i in range(len(dfchart) - 8):
                setValue = True
                for y in range(8):
                    item = dfchart.iloc[i + y][vargraph]
                    if abs(mean - item) < std:
                        setValue = False
                        break
                
                if setValue:
                    values[i+8] = 1
            
            data['rule_8'] = values

    label_title, label_y_axis = labeler(varname=varname)

    if vargraph == 'mean':
    
        result = {'all_values': x,
                'rule_1': [],
                'rule_2': [],
                'rule_3': [],
                'rule_4': [],
                'rule_5': [],
                'rule_6': [],
                'rule_7': [],
                'rule_8': [],
                'fda': outleirsresults,
                }
        
        applier = nelson()

        applier.rule1(result, mean_x, std_x)
        applier.rule2(result, mean_x)
        applier.rule3(result)
        applier.rule4(result)
        applier.rule5(result, mean_x, std_x)
        applier.rule6(result, mean_x, std_x)
        applier.rule7(result, mean_x, std_x)
        applier.rule8(result, mean_x, std_x)

        mark = 6.0
        mean3top = mean_x + 3*std_x
        mean3low = mean_x - 3*std_x
        mean2top = mean_x + 2*std_x
        mean2low = mean_x - 2*std_x
        mean1top = mean_x + std_x
        mean1low = mean_x - std_x
        
        fig, ax = plt.subplots(figsize=(18, 8))
    
        ax.set_title(label_title+r'$\bar{x}$'+f' chart')
        ax.set(xlabel='Date', ylabel=r'$\bar{x}' + label_y_axis)
        
        plt.plot(timestamps, result['all_values'], color='red', markevery=format_arr(1, result=result), ls='', marker='s', mfc='none', mec='red', label='Rule1', markersize=mark*5.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(2, result=result), ls='', marker='o', mfc='none', mec='blue', label="Rule2", markersize=mark*4.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(3, result=result), ls='', marker='o', mfc='none', mec='purple', label="Rule3", markersize=mark*4.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(4, result=result), ls='', marker='o', mfc='none', mec='green', label="Rule4", markersize=mark*3.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(5, result=result), ls='', marker='o', mfc='none', mec='orange', label='Rule5', markersize=mark*3.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(6, result=result), ls='', marker='o', mfc='none', mec='pink', label='Rule6', markersize=mark*2.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(7, result=result), ls='', marker='o', mfc='none', mec='cyan', label='Rule7', markersize=mark*2.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(8, result=result), ls='', marker='o', mfc='none', mec='olive', label='Rule8', markersize=mark*1.7)
        plt.plot(timestamps, result['all_values'], color='blue', marker="o", markersize=mark) # Comment to remove fda results
        # plt.plot(timestamps, result['all_values'], color='red', marker="o", markersize=mark, label='fda') # Comment out to include fda results
        # plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr_fda(result['fda']), marker="o", markersize=mark) # Comment out to include fda results

        plt.xticks(timestamps, fontsize = 8, rotation = 90)
        plt.grid(axis = 'x')

        left, right = ax.get_xlim()
        
        ax.text(right + 0.3, mean3top, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3top)), color='red')
        ax.text(right + 0.3, mean3low, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3low)), color='red')
        ax.text(right + 0.3, mean2top, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2top)), color='orange')
        ax.text(right + 0.3, mean2low, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2low)), color='orange')
        ax.text(right + 0.3, mean1top, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1top)), color='green')
        ax.text(right + 0.3, mean1low, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1low)), color='green')
        ax.text(right + 0.3, mean_x, r'$\bar{x}$' + '=' + str('{:.2f}'.format(mean_x)), color='black')
        
        plotAxlines(result['all_values'])

        if timeframe == 'a':
            ax.xaxis.set_major_locator(MultipleLocator(2))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        elif timeframe == 'b':
            ax.xaxis.set_major_locator(MultipleLocator(6))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        else:
            ax.xaxis.set_major_locator(MultipleLocator(8))
            ax.xaxis.set_minor_locator(MultipleLocator(1))

        plt.legend()
        # plt.legend(bbox_to_anchor=(1.15, 1), loc='upper left', borderaxespad=0.)

        # plt.savefig('control-chart.png')
        plt.show()
        
        # Validation
        # rule = str(input('Which Weco rule do you wish to validate (rule_#): '))
        # rule = 'rule_5'
        # outliers = validator(rule, timestamps)
        
        # print('outliers: ', outliers)
    
    elif vargraph == 'stds':
        
        result = {'all_values': s,
                'rule_1': [],
                'rule_2': [],
                'rule_3': [],
                'rule_4': [],
                'rule_5': [],
                'rule_6': [],
                'rule_7': [],
                'rule_8': [],
                'fda': outleirsresults,
                }
        
        applier = nelson()

        applier.rule1(result, mean_s, std_s)
        applier.rule2(result, mean_s)
        applier.rule3(result)
        applier.rule4(result)
        applier.rule5(result, mean_s, std_s)
        applier.rule6(result, mean_s, std_s)
        applier.rule7(result, mean_s, std_s)
        applier.rule8(result, mean_s, std_s)
        
        mark = 6.0
        mean3top = mean_s + 3*std_s
        mean3low = mean_s - 3*std_s
        mean2top = mean_s + 2*std_s
        mean2low = mean_s - 2*std_s
        mean1top = mean_s + std_s
        mean1low = mean_s - std_s
        
        fig, ax = plt.subplots(figsize=(12, 8))
    
        ax.set_title(r'$NO_2$' + ' s chart')
        ax.set(xlabel='Date', ylabel=r'$\sigma' + r' (\mu*g/m^3)$')
        
        plt.plot(timestamps, result['all_values'], color='red', markevery=format_arr(1, result=result), ls='', marker='s', mfc='none', mec='red', label='Rule1', markersize=mark*5.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(2, result=result), ls='', marker='o', mfc='none', mec='blue', label="Rule2", markersize=mark*4.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(3, result=result), ls='', marker='o', mfc='none', mec='purple', label="Rule3", markersize=mark*4.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(4, result=result), ls='', marker='o', mfc='none', mec='green', label="Rule4", markersize=mark*3.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(5, result=result), ls='', marker='o', mfc='none', mec='orange', label='Rule5', markersize=mark*3.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(6, result=result), ls='', marker='o', mfc='none', mec='pink', label='Rule6', markersize=mark*2.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(7, result=result), ls='', marker='o', mfc='none', mec='cyan', label='Rule7', markersize=mark*2.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(8, result=result), ls='', marker='o', mfc='none', mec='olive', label='Rule8', markersize=mark*1.7)
        plt.plot(timestamps, result['all_values'], color='red', marker="o", markersize=mark, label='fda')
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr_fda(result['fda']), marker="o", markersize=mark)
        plt.xticks(timestamps, fontsize = 8, rotation = 90)
        plt.grid(axis = 'x')

        left, right = ax.get_xlim()
        
        ax.text(right + 0.3, mean3top, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3top)), color='red')
        ax.text(right + 0.3, mean3low, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3low)), color='red')
        ax.text(right + 0.3, mean2top, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2top)), color='orange')
        ax.text(right + 0.3, mean2low, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2low)), color='orange')
        ax.text(right + 0.3, mean1top, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1top)), color='green')
        ax.text(right + 0.3, mean1low, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1low)), color='green')
        ax.text(right + 0.3, mean_s, r'$\bar{x}$' + '=' + str('{:.2f}'.format(mean_s)), color='black')
        
        plotAxlines(result['all_values'])

        if timeframe == 'a':
            ax.xaxis.set_major_locator(MultipleLocator(2))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        elif timeframe == 'b':
            ax.xaxis.set_major_locator(MultipleLocator(6))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        else:
            ax.xaxis.set_major_locator(MultipleLocator(4))
            ax.xaxis.set_minor_locator(MultipleLocator(1))

        plt.legend()
        # plt.legend(bbox_to_anchor=(1.15, 1), loc='upper left', borderaxespad=0.)

        # plt.savefig('control-chart.png')
        plt.show()
        
        # Validation
        # rule = str(input('Which Weco rule do you wish to validate (rule_#): '))
        # rule = 'rule_5'
        # outliers = validator(rule, timestamps)
        
        # print('outliers: ', outliers)
    
    elif vargraph == 'ranges':
        
        result = {'all_values': mr,
                'rule_1': [],
                'rule_2': [],
                'rule_3': [],
                'rule_4': [],
                'rule_5': [],
                'rule_6': [],
                'rule_7': [],
                'rule_8': [],
                'fda': outleirsresults,
                }
    
        applier = nelson()

        applier.rule1(result, mean_mr, std_mr)
        applier.rule2(result, mean_mr)
        applier.rule3(result)
        applier.rule4(result)
        applier.rule5(result, mean_mr, std_mr)
        applier.rule6(result, mean_mr, std_mr)
        applier.rule7(result, mean_mr, std_mr)
        applier.rule8(result, mean_mr, std_mr)
        
        mark = 6.0
        mean3top = mean_mr + 3*std_mr
        mean3low = mean_mr - 3*std_mr
        mean2top = mean_mr + 2*std_mr
        mean2low = mean_mr - 2*std_mr
        mean1top = mean_mr + std_mr
        mean1low = mean_mr - std_mr

        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.set_title(r'$NO_2$' ' mR chart')
        ax.set(xlabel='Date', ylabel='Variability' + r'$(\mu*g/m^3)$')
        
        plt.plot(timestamps, result['all_values'], color='red', markevery=format_arr(1, result=result), ls='', marker='s', mfc='none', mec='red', label='Rule1', markersize=mark*5.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(2, result=result), ls='', marker='o', mfc='none', mec='blue', label="Rule2", markersize=mark*4.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(3, result=result), ls='', marker='o', mfc='none', mec='purple', label="Rule3", markersize=mark*4.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(4, result=result), ls='', marker='o', mfc='none', mec='green', label="Rule4", markersize=mark*3.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(5, result=result), ls='', marker='o', mfc='none', mec='orange', label='Rule5', markersize=mark*3.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(6, result=result), ls='', marker='o', mfc='none', mec='pink', label='Rule6', markersize=mark*2.7)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(7, result=result), ls='', marker='o', mfc='none', mec='cyan', label='Rule7', markersize=mark*2.2)
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr(8, result=result), ls='', marker='o', mfc='none', mec='olive', label='Rule8', markersize=mark*1.7)
        plt.plot(timestamps, result['all_values'], color='red', marker="o", markersize=mark, label='fda')
        plt.plot(timestamps, result['all_values'], color='blue', markevery=format_arr_fda(result['fda']), marker="o", markersize=mark)
        plt.xticks(timestamps, fontsize = 8, rotation = 90)
        plt.grid(axis = 'x')

        left, right = ax.get_xlim()
        
        ax.text(right + 0.3, mean3top, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3top)), color='red')
        ax.text(right + 0.3, mean3low, r'$3\sigma$' + '=' + str('{:.2f}'.format(mean3low)), color='red')
        ax.text(right + 0.3, mean2top, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2top)), color='orange')
        ax.text(right + 0.3, mean2low, r'$2\sigma$' + '=' + str('{:.2f}'.format(mean2low)), color='orange')
        ax.text(right + 0.3, mean1top, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1top)), color='green')
        ax.text(right + 0.3, mean1low, r'$\sigma$' + '=' + str('{:.2f}'.format(mean1low)), color='green')
        ax.text(right + 0.3, mean_mr, r'$\bar{x}$' + '=' + str('{:.2f}'.format(mean_mr)), color='black')
        
        plotAxlines(result['all_values'])
        
        if timeframe == 'a':
            ax.xaxis.set_major_locator(MultipleLocator(2))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        elif timeframe == 'b':
            ax.xaxis.set_major_locator(MultipleLocator(6))
            ax.xaxis.set_minor_locator(MultipleLocator(1))
        else:
            ax.xaxis.set_major_locator(MultipleLocator(4))
            ax.xaxis.set_minor_locator(MultipleLocator(1))

        plt.legend()
        # plt.legend(bbox_to_anchor=(1.15, 1), loc='upper left', borderaxespad=0.)

        # plt.savefig('control-chart.png')
        plt.show()
        
        # Validation
        # rule = str(input('Which Weco rule do you wish to validate (rule_#): '))
        # rule = 'rule_5'
        # outliers = validator(rule, timestamps)
        
        # print('outliers: ', outliers)