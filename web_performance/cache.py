from django.conf import settings
from django.middleware.cache import FetchFromCacheMiddleware, UpdateCacheMiddleware
from django.test.client import Client

def remove_fetch_middleware():
    """ We can remove this middleware safely as it works only as process_request
    """
    fetch_from_cache_middleware = 'django.middleware.cache.FetchFromCacheMiddleware'
    middleware_classes = list(settings.MIDDLEWARE_CLASSES)
    if fetch_from_cache_middleware in middleware_classes:
        middleware_classes.remove(fetch_from_cache_middleware)
        settings.MIDDLEWARE_CLASSES = middleware_classes

def update_cache(url, **options):
    """ Warm up cache or update it before there is a cache miss"""
    remove_fetch_middleware()

    client = Client(WEBPERF_FORCE_CACHE_UPDATE=True, **options)
#    client.handler._cache_update_cache = True
    response = client.get(url)
    response.render()


class UpdateCacheMiddleware(UpdateCacheMiddleware):
    """ Webperf version of django standard middleware
    """


class FetchFromCacheMiddleware(FetchFromCacheMiddleware):
    """ Webperf version of django standard middleware
    """

    def process_request(self, request):
        """ Forces caching"""
        if request.META.get('WEBPERF_FORCE_CACHE_UPDATE', False):
            request._cache_update_cache = True
            return None
        super(FetchFromCacheMiddleware, self).process_request(request)