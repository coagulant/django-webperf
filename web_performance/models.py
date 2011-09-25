from appconf import AppConf

class MyAppConf(AppConf):
    DOMAINS_NUMBER = 2
    MEDIA_TEMPLATE = ''

    class Meta:
        prefix = 'webperf'