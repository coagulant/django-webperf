import hashlib
import os
import urlparse
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from django.conf import settings

class DomainShardingStorage(FileSystemStorage):
    """
    Standard filesystem storage with domain sharding for urls
    """
    def __init__(self, location=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.location = os.path.abspath(location)

    def get_domain_number_for_uri(self, uri):
        md5 = hashlib.md5()
        md5.update(uri)
        integer_hash = int(md5.hexdigest(), 16)
        domain_number = integer_hash % settings.WEBPERF_DOMAINS_NUMBER + 1
        return domain_number

    def url(self, name):
        filepath = filepath_to_uri(name)
        domain_number = self.get_domain_number_for_uri(filepath)
        sharded_base_url = settings.WEBPERF_MEDIA_TEMPLATE.format(domain_number)
        return urlparse.urljoin(sharded_base_url, filepath)
