import hashlib
import urlparse
from django.core.files.storage import FileSystemStorage

class DomainShardingStorage(FileSystemStorage):
    """
    Standard filesystem storage with domain sharding for urls
    """
    DOMAINS_NUMBER = 2
    DOMAIN_TEMPLATE = 'http://img{0}.futurecolors.ru'

    def get_domain_number_for_uri(self, uri):
        md5 = hashlib.md5()
        md5.update(uri)
        integer_hash = int(md5.hexdigest(), 16)
        domain_number = integer_hash % self.DOMAINS_NUMBER + 1
        return domain_number

    def get_sharded_url(self, name):
        filepath = filepath_to_uri(name)
        sharded_base_url = self.DOMAIN_TEMPLATE.format(self.get_domain_number_for_uri(uri))
        return urlparse.urljoin(sharded_base_url, self.base_url, filepath)

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return self.get_sharded_url(name)
