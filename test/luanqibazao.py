import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
"""
print data to csv file
"""
# names = ['Bob', 'Jessica', 'Mary', 'John', 'Mel']
# births = [968, 155, 77, 578, 973]
#
# df = pd.DataFrame()
# df['Names'] = names
# df['Births'] = births
#
# print(df)
# df.to_csv(r'd:\births1880.csv', index=False)

"""
read data from csv
"""
# df = pd.read_csv(r'd:\births1880.csv')
# sorted_df = df.sort_values(['Births'], ascending=False)
# print(sorted_df.head(2))
# print(df.max())

np.random.seed(111)


# data maker
def create_data_set(number=1):
    output = []

    for i in range(number):
        rng = pd.date_range(start='2009/1/1', end='2012/12/31', freq='W-MON')
        data = np.random.randint(low=30, high=1000, size=len(rng))

        status_pool = [1, 2, 3]

        random_status = [status_pool[np.random.randint(low=0, high=len(status_pool))] for j in range(len(rng))]

        state_pool = ['A', 'B', 'C', 'D', 'E', 'F']

        random_state = [state_pool[np.random.randint(low=0, high=len(state_pool))] for j in range(len(rng))]

        output.extend(zip(random_state, random_status, data, rng))

    return output


# data_set = create_data_set(4)
# df = pd.DataFrame(data=data_set, columns=['State', 'Status', 'Count', 'Date'])
# df.to_csv(r"d:\lesson\lesson3.csv", index=False)
df = pd.read_csv(r"d:\lesson\lesson3.csv", parse_dates=['Date'], index_col='Date')
df['State'] = df.State.apply(lambda x: x.lower())
mask = df['Status'] == 1
df = df[mask]

mask = ((df['State'] == 'b') | (df['State'] == 'd'))
df['State'][mask] = 'db'
# df['Count'].plot(figsize=(15, 5))
# plt.show()
# sorted_by_state = df[df['State'] == 'a'].sort_index(axis=0)
# print(sorted_by_state.head())
daily = df.reset_index().groupby(['State', 'Date']).sum()
del daily['Status']
# daily.loc['db']['2011':].plot(figsize=(15, 5))
# plt.show()
state_year_month = daily.groupby([daily.index.get_level_values(0), daily.index.get_level_values(1).year,
                                  daily.index.get_level_values(1).month])
daily['lower'] = state_year_month['Count'].transform(lambda x: x.quantile(q=.25) - (1.5*x.quantile(q=.75)-x.quantile(q=.25)))
daily['higher'] = state_year_month['Count'].transform(lambda x: x.quantile(q=.75) + (1.5*x.quantile(q=.75)-x.quantile(q=.25)))
daily['outlier'] = (daily['Count'] < daily['lower']) | (daily['Count'] > daily['higher'])

daily = daily[daily['outlier'] == False]

all = pd.DataFrame()
all['Count'] = daily['Count'].groupby(daily.index.get_level_values(1)).sum()
# print(all.index)
year_month = all.groupby([lambda x: x.year, lambda x: x.month])
# year_month = all.groupby([all.index.year, all.index.month])
# print(year_month.max())
all['max'] = year_month['Count'].transform(lambda x: x.max())
# print(all.head())
data = [1000, 2000, 3000]
idx = pd.date_range(start='2011/12/31', end='2013/12/31', freq='A')
bhag = pd.DataFrame(data, index=idx, columns=['BHAG'])

combined = pd.concat([all, bhag])
combined = combined.sort_index(axis=0)
# print(combined.tail())
year = combined.groupby(lambda x: x.year).sum()
year['pct'] = year['max'].pct_change(periods=1)
year.loc[2013, 'max'] = (1 + year.loc[2012, 'pct']) * year.loc[2012, 'max']
year.loc[2013, 'pct'] = (year.loc[2013, 'max'] - year.loc[2012, 'max']) / year.loc[2012, 'max']
print(daily)
all['max'].plot(figsize=(10, 5))
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
fig.subplots_adjust(hspace=1.0)
daily.loc['a']['Count']['2012':].fillna(method='pad').plot(ax=axes[0, 0])
daily.loc['e']['Count']['2012':].fillna(method='pad').plot(ax=axes[0, 1])
daily.loc['c']['Count']['2012':].fillna(method='pad').plot(ax=axes[1, 0])
daily.loc['f']['Count']['2012':].fillna(method='pad').plot(ax=axes[1, 1])

plt.show()
