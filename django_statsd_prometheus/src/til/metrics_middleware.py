import time
from datadog import DogStatsd
import time
import sys
from django.db.models.signals import post_save
from django.db.backends.signals import connection_created
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from django.dispatch import receiver
from django.core.cache.backends import locmem


statsd = DogStatsd(host="statsd", use_ms=True, port=9125)

REQUEST_LATENCY_METRIC_NAME = 'django_request_latency_ms'
REQUEST_COUNT_METRIC_NAME = 'django_request_count'
DJANGO_EXCEPTION_COUNTER = 'django_exceptions'
DJANGO_MODELS_NEW_ROW_METRIC_NAME = 'django_models_create_count'
DJANGO_MODELS_UPDATE_ROW_METRIC_NAME = 'django_models_update_count'
DJANGO_DB_CONNECTIONS_CREATED_METRIC_NAME = 'django_database_connections_count'
DJANGO_USER_LOGIN_METRIC_NAME = 'django_user_login'
DJANGO_LOCAL_CACHE_METRIC_NAME = 'django_cache_localmem'

@receiver(post_save)
def update_models_save_counter(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        statsd.increment(DJANGO_MODELS_NEW_ROW_METRIC_NAME,
            tags=[
                'model:%s' % sender,
                'using:%s' % using,
            ]
        )
    else:
        statsd.increment(DJANGO_MODELS_UPDATE_ROW_METRIC_NAME,
            tags=[
                'model:%s' % sender,
                'using:%s' % using,
            ]
        )

@receiver(connection_created)
def update_connection_created_metric(sender, connection, **kwargs):
    
    statsd.increment(DJANGO_DB_CONNECTIONS_CREATED_METRIC_NAME,
        tags=[
            'sender:%s' % sender,
            'connection:%s' % connection.display_name,
        ]
    )


@receiver(user_logged_in)
def update_user_logged_in_metric(sender, request, user, **kwargs):
    
    statsd.increment(DJANGO_USER_LOGIN_METRIC_NAME,
        tags=[
            'operation:login',
        ]
    )

@receiver(user_logged_out)
def update_user_logged_out_metric(sender, request, user, **kwargs):
    
    statsd.increment(DJANGO_USER_LOGIN_METRIC_NAME,
        tags=[
            'operation:logout',
        ]
    )

@receiver(user_login_failed)
def update_user_failed_login_metric(sender, credentials, request, **kwargs):
    
    statsd.increment(DJANGO_USER_LOGIN_METRIC_NAME,
        tags=[
            'operation:login_failed',
        ]
    )

class InstrumentedLocMemCache(locmem.LocMemCache):

    def get(self, key, default=None, version=None):
        statsd.increment(DJANGO_LOCAL_CACHE_METRIC_NAME,
            tags=[
                'operation:get',
                'item:%s' % key,
            ]
        )
        v = super(InstrumentedLocMemCache, self).get(key, default=None, version=version)
        if v is not None:
            statsd.increment(DJANGO_LOCAL_CACHE_METRIC_NAME,
            tags=[
                'operation:hit',
                'item:%s' % key,
            ]
        )
        else:
            statsd.increment(DJANGO_LOCAL_CACHE_METRIC_NAME,
            tags=[
                'operation:miss',
                'item:%s' % key,
            ]
        )
        return v or default
    

class StatsdReporter():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        statsd.increment(REQUEST_COUNT_METRIC_NAME,
                tags=[
                    'endpoint:%s' % request.path_info,
                    'method:%s' % request.method,
                ]
        )

        response = self.get_response(request)
        if response:
            resp_time = (time.time() - request.start_time)*1000
            statsd.timing(REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                tags=[
                    'endpoint:%s' % request.path_info,
                    'view_name:%s' % getattr(request, 'view_func_name', 'unknown'),
                    'method:%s' % request.method,
                    'status:%s' % str(response.status_code)
                ]
            )
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'resolver_match') and request.resolver_match is not None:
            request.view_func_name = request.resolver_match.func.__name__
        else:
            request.view_func_name = "unknown"
       
        return None

    def process_exception(self, request, exception):
        statsd.increment(DJANGO_EXCEPTION_COUNTER,
            tags=[
                    'endpoint:%s' % request.path_info,
                    'method:%s' % request.method,
                    'exception_class:%s' % exception.__class__,
            ]
        )