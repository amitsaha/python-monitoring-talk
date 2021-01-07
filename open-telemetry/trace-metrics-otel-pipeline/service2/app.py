from opentelemetry import metrics, trace

from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace import sampling
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)

from opentelemetry.exporter.opencensus.metrics_exporter import (
    OpenCensusMetricsExporter,
)
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask, request

import mysql.connector
from opentelemetry.instrumentation.mysql import MySQLInstrumentor

import os


resource = Resource({"service.name": "service2"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

OTEL_AGENT = os.getenv('OTEL_AGENT', "otel-agent")

otlp_exporter = OTLPSpanExporter(endpoint=OTEL_AGENT + ":4317", insecure=True)
span_processor = BatchExportSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


metric_exporter = OpenCensusMetricsExporter(
    endpoint=OTEL_AGENT + ":55678",
    service_name="service2",
)

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider(resource=resource))
meter = metrics.get_meter(__name__)
# controller collects metrics created from meter and exports it via the
# exporter every interval
controller = PushController(meter, metric_exporter, 5)

# TODO: We use a different metric name here due to:
# https://github.com/open-telemetry/opentelemetry-python/issues/1510
requests_counter = meter.create_counter(
    name="requests_count_service2",
    description="number of requests",
    unit="1",
    value_type=int,
)
# Labels are used to identify key-values that are associated with a specific
# metric that you want to record. These are useful for pre-aggregation and can
# be used to store custom dimensions pertaining to a metric
labels = {"service_id": "service2"}


app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
MySQLInstrumentor().instrument()

@app.route('/')
def index():
    requests_counter.add(1, labels)
    with tracer.start_as_current_span("service2-db"):
        # TODO - Move this to app initialization rather than per request
        cnx = mysql.connector.connect(user='joe', password='password',
                                host='db',
                                database='service2')
        data = "<h1>Data</h1><p><table>{0}</table></p>"
        cursor = cnx.cursor()
        cursor.execute("SELECT first_name, last_name from users")
        rows = ""
        for first_name, last_name in cursor:
            rows += '<tr><td>{0}</td><td>{1}</td></tr>'.format(first_name, last_name)
    return data.format(rows), 200

if __name__ == '__main__':
    app.run(debug=True)
