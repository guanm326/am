from WindPy import w
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CLOSE = 'CLOSE'
w.start()

wsd_data = w.wsd("000001.SZ", "open,high,low,close", "2017-08-30", "2017-09-30", "Fill=Previous")

fm = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Times)
fm = fm.T

tech_rets = fm.pct_change()
rets = tech_rets.dropna()

days = 365
dt = 1. / days
mu = rets[CLOSE].mean()
sigma = rets[CLOSE].std()
start_price = 11.53


def stock_monte_carlo(start_price, days, mu, sigma):
    price = np.zeros(days)
    price[0] = start_price
    shock = np.zeros(days)
    drift = np.zeros(days)

    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
        drift[x] = mu * dt
        price[x] = price[x-1] + (price[x-1] * (drift[x] + shock[x]))

    return price


runs = 10000
simulations = np.zeros(runs)
for run in range(runs):
    simulations[run] = stock_monte_carlo(start_price, days, mu, sigma)[days-1]

q = np.percentile(simulations, 1)
plt.hist(simulations, bins=200)
plt.figtext(0.6, 0.8, s="Start price: %.2f" % start_price)
plt.figtext(0.6, 0.7, "Mean final price: %.2f" % simulations.mean())
plt.figtext(0.6, 0.6, "VaR(0.99): %.2f" % (start_price - q,))
plt.figtext(0.15, 0.6, "q(0.99): %.2f" % q)
plt.axvline(x=q, linewidth=4, color='r')
plt.title(u"Final price distribution for 600050 after %s days" % days, weight='bold')
plt.show()

w.stop()
