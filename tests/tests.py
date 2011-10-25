from django.conf import settings
from django.core.cache import cache, get_cache
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.cache import get_cache_key, _generate_cache_header_key
from mock import patch
from models import Example1, Example2
from web_performance.cache import FetchFromCacheMiddleware
from web_performance.storage import DomainShardingStorage


class FetchFromCacheMiddlewareTestCase(TestCase):
    RESPONSE_CACHED_VALUE = 'Response value'

    def setUp(self):
        self.middleware = FetchFromCacheMiddleware()
        self.factory = RequestFactory()
        self.request = RequestFactory().get('/')

    def warmup_cache(self):
        cache = get_cache(settings.CACHE_MIDDLEWARE_ALIAS)
        cache_header_key = _generate_cache_header_key(settings.CACHE_MIDDLEWARE_KEY_PREFIX, self.request)
        cache.set(cache_header_key, 'header dummy cache', 30)
        cache_key = get_cache_key(self.request,
                                  settings.CACHE_MIDDLEWARE_KEY_PREFIX, 'GET',
                                  cache=cache)
        cache.set(cache_key, self.RESPONSE_CACHED_VALUE, 30)

    def test_cold_cache_regular_request(self):
        result = self.middleware.process_request(self.request)
        self.assertTrue(self.request._cache_update_cache)
        self.assertEqual(result, None)

    def test_warmedup_cache_regular_request(self):
        self.warmup_cache()
        result = self.middleware.process_request(self.request)
        self.assertFalse(self.request._cache_update_cache)
        self.assertEqual(result, self.RESPONSE_CACHED_VALUE)

    def test_cold_cache_request_force_cache(self):
        request = self.factory.get('/', WEBPERF_FORCE_CACHE_UPDATE=True)
        result = self.middleware.process_request(request)
        self.assertTrue(request._cache_update_cache)
        self.assertEqual(result, None)

    def test_warmedup_cache_request_force_cache(self):
        self.warmup_cache()
        request = self.factory.get('/', WEBPERF_FORCE_CACHE_UPDATE=True)
        result = self.middleware.process_request(request)
        self.assertTrue(request._cache_update_cache)
        self.assertEqual(result, None)


@patch.object(settings, 'WEBPERF_DOMAINS_NUMBER', 2)
@patch.object(settings, 'WEBPERF_MEDIA_TEMPLATE', 'http://img{0}.example.com/media/')
class DomainShardingTestCase(TestCase):

    def test_domain_number_for_url(self):
        storage = DomainShardingStorage()

        domain_numbers = set([storage.get_domain_number_for_uri('avatars/{0}.jpg'.format(i)) for i in xrange(100)])

        self.assertTrue(len(domain_numbers), settings.WEBPERF_DOMAINS_NUMBER)
        for i in xrange(1, settings.WEBPERF_DOMAINS_NUMBER+1):
            self.assertTrue(i in domain_numbers)

    def test_sharded_url(self):
        storage = DomainShardingStorage()
        urls = [storage.url('images/example{0}.jpg'.format(i)) for i in xrange(100)]

        for url in urls:
            self.assertRegexpMatches(url, r'http://img\d+\.example\.com/media/images/example\d+\.jpg')

    @patch.object(settings, 'DEFAULT_FILE_STORAGE', 'web_performance.storage.DomainShardingStorage')
    def test_filefield_with_alternative_default_storage(self):
        instance = Example1()
        instance.file.name = 'files/example.jpg'

        self.assertEqual(instance.file.url, 'http://img1.example.com/media/files/example.jpg')

    def test_filefield_with_customized_storage(self):
        instance = Example2()
        instance.file.name = 'files/example.jpg'

        self.assertEqual(instance.file.url, 'http://img1.example.com/media/files/example.jpg')


class DomainShardingNotConfiguredTestCase(TestCase):

    def test_not_configured(self):
        storage = DomainShardingStorage()
        url = storage.url('images/example.jpg')
        self.assertEqual(url, 'images/example.jpg')