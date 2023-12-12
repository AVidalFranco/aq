import numpy as np

from kneed import KneeLocator
from matplotlib import pyplot as plt
plt.style.use('ggplot')
from statsmodels.distributions.empirical_distribution import ECDF

# This website has representation tools for bivariate distributions
# https://seaborn.pydata.org/tutorial/distributions.html#empirical-cumulative-distributions

def is_even(num):
    return num % 2 == 0

def empirical_cdf(data):

    ecdf = ECDF(data)

    x = np.linspace(min(data), max(data), num=len(data))
    y = ecdf(x)

    # Plot the results
    # plt.step(x, y)
    # plt.show()

    # x is the data that we need to calculate the distance between cdf (data and generated)

    return x, y

def outDec(magnitude, shape, detection_threshold):
    
    """This function analyzes if there are outliers in the data"""
    
    # Get the empirial cdf of mag and shape
    magnitude_cdf, y_magnitude = empirical_cdf(magnitude)
    shape_cdf, y_shape = empirical_cdf(shape)
    
    # # Plot the empirical cdf of mag
    # fig, axes = plt.subplots(1, 1, figsize=(7, 5))
    # plt.step(magnitude_cdf, y_magnitude, label='Magnitude', axes=axes)
    # axes.legend(loc='best')
    # axes.set(xlabel='Magnitude', ylabel='p', title='Magnitude cumulative distribution function')
    # plt.show()
    
    # # Plot the empirial cdf of shape
    # fig, axes = plt.subplots(1, 1, figsize=(7, 5))
    # plt.step(shape_cdf, y_shape, label='Shape', axes=axes)
    # axes.legend(loc='best')
    # axes.set(xlabel='Shape', ylabel='p', title='Shape cumulative distribution function')
    # plt.show()

    # Convert arrays to list so I can use pop() and sort them
    magnitude, shape = list(sorted(magnitude)), list(sorted(shape))

    # Get the distance between the extreme points in mag and in shape
    distance_magnitude, distance_shape = abs(magnitude[-1] - magnitude[0]), abs(shape[-1] - shape[0])
    
    # Get mag crushing data
    magnitude_crushed = []
    for i in range(len(magnitude)-1):
        if is_even(i) == True:
            magnitude.pop(-1)
            distance_magnitude_updated = abs(magnitude[-1] - magnitude[0])

        elif is_even(i) == False:
            magnitude.pop(0)
            distance_magnitude_updated = abs(magnitude[-1] - magnitude[0])
        
        magnitude_crushed.append(np.round((distance_magnitude_updated/distance_magnitude) * 100, 3))
    
    # Get shape crushed data
    shape_crushed = []
    for i in range(len(shape)-1):
        shape.pop(-1)
        distance_shape_updated = abs(shape[-1] - shape[0])
        
        shape_crushed.append(np.round((distance_shape_updated/distance_shape) * 100, 3))
    
    # Plot the crushed mag and shape
    # plt.plot(magnitude_crushed, np.arange(0, len(magnitude_crushed)), label = 'magnitude')
    # plt.plot(shape_crushed, np.arange(0, len(shape_crushed)), label = 'shape')
    # plt.title('Crushed magnitude, and shape)
    # plt.legend(loc='best')
    # plt.show()

    # Get the point where the elbow/knee starts flattening
    kl_magnitude = KneeLocator(magnitude_crushed, np.arange(0, len(magnitude_crushed)), curve='convex', direction='decreasing')
    kl_magnitude_point = kl_magnitude.knee
    # kl_magnitude.plot_knee()
    # plt.show()

    kl_shape = KneeLocator(shape_crushed, np.arange(0, len(shape_crushed)), curve='convex', direction='decreasing')
    kl_shape_point = kl_shape.knee
    # kl_shape.plot_knee()
    # plt.show()

    print('Magnitude knee:', kl_magnitude_point, 'Shape knee:', kl_shape_point)

    # Define wether there are outliers or not in the data based on the value of the knee/elbow points
    if (kl_magnitude_point is None) and (kl_shape_point is None):
        outliers_in_data = False
    else:
        if (kl_magnitude_point is None):
            kl_magnitude_point = 100
        if (kl_shape_point is None):
            kl_shape_point = 100
        if (kl_magnitude_point <= detection_threshold) or (kl_shape_point <= detection_threshold):
            outliers_in_data = True
        else:
            outliers_in_data = False
    
    return outliers_in_data