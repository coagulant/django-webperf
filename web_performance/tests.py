import logging
from django.test import TestCase
from web_performance.storage import DomainShardingStorage

class TwitterTagTestCase(TestCase):

    def test_domain_number_for_url(self):
        storage = DomainShardingStorage()

        domain_numbers = set([storage.get_domain_number_for_uri('avatars/{0}.jpg'.format(i)) for i in xrange(100)])

        self.assertFalse(0 in domain_numbers)
        self.assertTrue(1 in domain_numbers)
        self.assertTrue(2 in domain_numbers)
        self.assertFalse(4 in domain_numbers)