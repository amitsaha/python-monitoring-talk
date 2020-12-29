from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace import sampling
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)

from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from flask import Flask, request
import requests

trace.set_tracer_provider(TracerProvider(sampler=sampling.ALWAYS_ON))

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="service1",
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

def do_stuff():
    return requests.get('http://service2:5000')

@app.route('/')
def index():
    with tracer.start_as_current_span("service2-request"):
        data = do_stuff()
    return data.text, 200

if __name__ == '__main__':
    app.run(debug=True)

