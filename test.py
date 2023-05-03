import numpy as np
from matplotlib import pyplot as plt

varName = 'pH'
clean = True

mag, shape = np.load(f'Data_mag_shape/{varName}_mag.npy'), np.load(f'Data_mag_shape/{varName}_shape.npy')
print(mag, shape, len(mag), len(shape))

plt.scatter(mag, shape)
plt.show()

if clean == True:
    mag_upper = np.percentile(mag, 75)
    mag_lower = np.percentile(mag, 25)
    # mag = list(filter(lambda x: (x <= (np.percentile(mag, 75))) or (x >= (np.percentile(mag, 25))), mag))
    mag = list(filter(lambda x: x <= mag_upper, mag))
    mag = list(filter(lambda x: x >= mag_lower, mag))
    shape = list(filter(lambda x: x <= (np.percentile(shape, 50)), shape))

    print(mag, shape, len(mag), len(shape))

    plt.scatter(mag, shape)
    plt.show()
