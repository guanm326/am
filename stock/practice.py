import pandas as pd
import numpy as np

a = np.arange(12).reshape(3, 4)

b1 = np.array([False, True, True])
b2 = np.array([True, False, True, False])
print(a[b1, b2])
