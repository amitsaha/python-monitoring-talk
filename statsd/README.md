# Reporting metrics to statsd

This demo builds upon Demos 1 and 2 to switch out writing metrics to a CSV file with
reporting to a `statsd` instance. It demonstrates:

- Adding *characteristics* to metrics by using `nested.keys`
- Graphite is setup as the storage backend for statsd 

## Adding characteristics to metrics

We update the [middlware.py](./src/helpers/middleware.py) to report metrics to `statsd` as follows:


```
statsd = statsd.StatsClient(host='statsd', port=8125, prefix='webapp1')

# request.<path>.<method>.http_<status_code>.latency
REQUEST_LATENCY_METRIC_KEY_PATTERN = 'instance1.{0}.{1}.http_{2}.latency'

# request.<path>.<method>.http_<status_code>
REQUEST_COUNT_METRIC_KEY_PATTERN = 'instance1.request.{0}.{1}.http_{2}.count'

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    key = REQUEST_LATENCY_METRIC_KEY_PATTERN.format(
        request.endpoint,
        request.method,
        response.status_code,
    )
    statsd.timing(key, resp_time)

    key = REQUEST_COUNT_METRIC_KEY_PATTERN.format(
        request.endpoint,
        request.method,
        response.status_code,
    )
    statsd.incr(key)
    return response
..
```


## Run demo

```
$ sudo docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

## Play with the data

If we now go to the address `http://<VM IP address>>` on  your host machine, you will
see a [graphite browser window](http://graphite.readthedocs.io/en/latest/overview.html).

Once you are there, we can play with the metrics that our application pushed.
