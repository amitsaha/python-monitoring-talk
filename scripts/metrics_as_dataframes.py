import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# seed values
app_prefix= ['webapp']
node_ids = ['10.1.1.30', '10.3.2.30']
http_endpoints = ['test1', 'test2']
http_methods = ['POST', 'GET']
http_statuses = ['200', '400', '500']
timestamps = pd.date_range('25/3/2018', periods=10000, freq='10S')
timestamps_unix = timestamps.view('int64') // pd.Timedelta(1, unit='s')

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
rolling_average = metrics.rolling(window=5000, center=False, on='latency').mean()
rolling_average.plot(title='Rolling average over 30 seconds', use_index=True)

# Histogram plot of latency
metrics.plot.hist(y='latency')
plt.show()
