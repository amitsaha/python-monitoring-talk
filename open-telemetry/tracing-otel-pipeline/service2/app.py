from opentelemetry import trace

from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace import sampling
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask, request

import mysql.connector
from opentelemetry.instrumentation.mysql import MySQLInstrumentor


resource = Resource({"service.name": "service2"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="otel-agent:4317", insecure=True)
span_processor = BatchExportSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
MySQLInstrumentor().instrument()

@app.route('/')
def index():
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
