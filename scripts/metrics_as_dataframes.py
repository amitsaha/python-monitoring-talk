import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# seed values
app_prefix= ['webapp']
node_ids = ['10.1.1.30', '10.3.2.30']
http_endpoints = ['test1', 'test2']
http_methods = ['POST', 'GET']
http_statuses = ['200', '400', '500']
# FIXME: the following leads to negative timestamps when plotted in
# matplotlib
# timestamps = pd.date_range('25/3/2018', periods=10000, freq='10S')
# timestamps_unix = timestamps.view('int') // pd.Timedelta(1, unit='s')

timestamps_unix = [time.time() for _ in range(10000)]

metrics = pd.DataFrame({
    'app_prefix': [app_prefix[random.choice(range(len(app_prefix)))] for _ in range(10000)],
    'node_id': [node_ids[random.choice(range(len(node_ids)))] for _ in range(10000)],
    'http_endpoint': [http_endpoints[random.choice(range(len(http_endpoints)))] for _ in range(10000)],
    'http_method': [http_methods[random.choice(range(len(http_methods)))] for _ in range(10000)],
    'http_status':[http_statuses[random.choice(range(len(http_statuses)))] for _ in range(10000)],
    'latency': np.random.normal(5000, 1000, 10000),
    }, index=timestamps_unix)


print(metrics)

print('\n\nMean Latency grouped by node and HTTP status\n\n')
print(metrics.groupby(['node_id', 'http_status']).latency.aggregate(np.mean))

print('\n\n99.999 percentile Latency grouped by node and HTTP status\n\n')
print(metrics.groupby(['node_id', 'http_status']).latency.aggregate(np.percentile, 99.999))

print('\n\n99.999 percentile Latency grouped by HTTP endpoint\n\n')
print(metrics.groupby(['http_endpoint', 'http_method']).latency.aggregate(np.percentile, 99))

plt.xkcd()
# Rolling average
latency = metrics['latency']
rolling_average = latency.rolling(window=100, center=False, min_periods=1).mean()
print(rolling_average)
rolling_average.plot(title='Rolling average over 100 observations', use_index=True)

# Histogram plot of latency
metrics.plot.hist(y='latency')
plt.show()
