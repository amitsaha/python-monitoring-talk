# Python prometheus client

## Gauge and Python multiprocess mode

If you look at https://github.com/prometheus/client_python#multiprocess-mode-gunicorn, there are various modes for gauge:

> Gauges have several modes they can run in, which can be selected with the multiprocess_mode parameter.

>   'all': Default. Return a timeseries per process alive or dead.
>    'liveall': Return a timeseries per process that is still alive.
>    'livesum': Return a single timeseries that is the sum of the values of alive processes.
>    'max': Return a single timeseries that is the maximum of the values of all processes, alive or dead.
>    'min': Return a single timeseries that is the minimum of the values of all processes, alive or dead.

If you see your gauge metrics being reported with a PID label, try using one of the other modes (based on https://github.com/prometheus/client_python/blob/master/prometheus_client/multiprocess.py)

# StatsD Exporter


## Things to keep in mind

The following are things to keep in mind while using the statsd exporter:

- No persistent storage in statsd exporter, it dies, you don't get metrics
- When using multiple statsd exporter instances, you may want to use a prometheus histogram rather than 
  summary (This [blog post](https://signoz.io/blog/quantile-aggregation-for-statsd-exporter/) explains why)

If you are using the DogStatsd Python client:

- Report all timing metrics in milliseconds
- If you are using the `timed()` context manager, initialize the statstd client using `use_ms`
