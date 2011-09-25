from django.conf import settings
from django.test import TestCase
from mock import patch
from models import Example1, Example2
from web_performance.storage import DomainShardingStorage

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