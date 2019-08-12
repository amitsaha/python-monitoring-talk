from flask import request
import statsd
import time
import sys

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

def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(stop_timer)
