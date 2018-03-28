from flask import Flask
from helpers.middleware import setup_metrics
import csv
import random

app = Flask(__name__)
setup_metrics(app)


@app.route('/test/')
def test():
    if random.random() < 0.8:
        return 'rest'
    else:
        return 'Bad Request', 400


@app.route('/test1/')
def test1():
    1/0
    return 'rest'


@app.errorhandler(500)
def handle_500(error):
    return str(error), 500


if __name__ == '__main__':
    with open('metrics.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['timestamp', 'app_prefix', 'node_id',
                            'http_endpoint', 'http_method', 'http_status',
                            'latency'])

    app.run(host="0.0.0.0")
