from appconf import AppConf

class MyAppConf(AppConf):
    DOMAINS_NUMBER = 2
    MEDIA_TEMPLATE = 'http://img{0}.example.com/media/'

    class Meta:
        prefix = 'webperf'