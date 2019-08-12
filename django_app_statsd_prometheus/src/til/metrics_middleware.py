import time
from datadog import DogStatsd
import time
import sys


statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'
REQUEST_COUNT_METRIC_NAME = 'request_count'

class StatsdReporter():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        view_name = "unknown"
        print(dir(request))
        if hasattr(request, 'resolver_match') and request.resolver_match is not None:
            view_name = request.resolver_match.func
            print(str(request.resolver_match))
        import sys; sys.stdout.flush()
        
        request.start_time = time.time()
        statsd.increment(REQUEST_COUNT_METRIC_NAME,
                tags=[
                    'endpoint:%s' % request.path_info,
                    'view_name:%s' % view_name,
                    'method:%s' % request.method,
                ]
        )

        response = self.get_response(request)
        if response:
            resp_time = time.time() - request.start_time
            
            statsd.timing(REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                tags=[
                    'endpoint:%s' % request.path_info,
                    'view_name:%s' % view_name,
                    'method:%s' % request.method,
                    'status:%s' % str(response.status_code)
                ]
            )
        return response
