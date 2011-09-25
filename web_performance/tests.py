from django.conf import settings
from django.test import TestCase
from mock import patch
from web_performance.storage import DomainShardingStorage

class TwitterTagTestCase(TestCase):

    @patch.object(settings, 'WEBPERF_DOMAINS_NUMBER', 5)
    @patch.object(settings, 'WEBPERF_DOMAIN_TEMPLATE', 'http://img{0}.example.com/media/')
    def test_domain_number_for_url(self):
        storage = DomainShardingStorage()

        domain_numbers = set([storage.get_domain_number_for_uri('avatars/{0}.jpg'.format(i)) for i in xrange(100)])

        self.assertTrue(len(domain_numbers), settings.WEBPERF_DOMAINS_NUMBER)
        for i in xrange(1, settings.WEBPERF_DOMAINS_NUMBER+1):
            self.assertTrue(i in domain_numbers)


    def test_sharded_url(self):
        storage = DomainShardingStorage()
        url = storage.get_sharded_url('images/example.jpg')

        self.assertEqual(url, 'http://img1.example.com/media/images/example.jpg')