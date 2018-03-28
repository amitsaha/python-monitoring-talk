from flask import request
import csv
import time
import random

node_ids = ['10.0.1.1', '10.1.3.4']


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    node_id = node_ids[random.choice(range(len(node_ids)))]
    with open('metrics.csv', 'a', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([
            str(int(time.time())), 'webapp1', node_id,
            request.endpoint, request.method, str(response.status_code),
            str(resp_time)
        ])

    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(stop_timer)
