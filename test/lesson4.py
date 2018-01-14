import pandas as pd
import numpy as np

d = np.arange(10)
df = pd.DataFrame(d, columns=['Data'])
df['NewCol'] = 9
print(df.head(3))
