from flask import request
import csv
import time


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    with open('metrics.csv', 'a', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([str(int(time.time())), str(resp_time)])

    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(stop_timer)
