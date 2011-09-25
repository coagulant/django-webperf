from django.conf import settings
from django.test import TestCase
from django.template import Template, Context
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


class AssetsCollectorTestCase(TestCase):

    def test_collector_inline_and_include(self):
        tpl = '''{% load webperf_tags %}
                 {% collect_assets js %}
                 <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min.js"></script>
                 {% endcollect_assets %}
                 {% include "included_template.html" %}
              '''

        expected_content = ('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min.js"></script>' +
                           '<script type="text/javascript" src="http://yandex.st/rightjs/2.1.1/right-min.js"></script>')

        context = Context()
        template = Template(tpl)
        output = template.render(context)
        self.assertEqual(output.strip(), '', msg='Template is not polluted with tags')
        self.assertEqual(context['js'].value().strip(), expected_content, msg='js variable is populated')


    def test_collector_tow_includes_get_assets(self):
        tpl = '''{% load webperf_tags %}
                 {% collect_assets js %}{% endcollect_assets %}
                 {% include "included_template.html" %}
                 {% include "another_template.html" %}
                 {% get_assets js %}
              '''
        expected_content = ('<script type="text/javascript" src="http://yandex.st/rightjs/2.1.1/right-min.js"></script>' +
                            '<script type="text/javascript" src=" http://yandex.st/prototype/1.7.0.0/prototype.min.js"></script>')

        context = Context()
        template = Template(tpl)
        output = template.render(context)
        self.assertTrue(expected_content in output, msg='script tags are collected and rendered at bottom')

    def test_collector_css_js(self):
        tpl = '''{% load webperf_tags %}
                 {% collect_assets js %}{% endcollect_assets %}
                 {% collect_assets css %}{% endcollect_assets %}
                 {% include "included_template.html" %}
                 {% include "css_js_template.html" %}
                 TEST
                 {% get_assets js %}
                 {% get_assets css %}
              '''

        expected_content_js =  ('<script type="text/javascript" src="http://yandex.st/rightjs/2.1.1/right-min.js"></script>' +
                               '<script type="text/javascript" src="http://yandex.st/pure/2.48/pure.min.js"></script>' +
                               '<script type="text/javascript" src="http://yandex.st/raphael/1.5.2/raphael.min.js"></script>')

        expected_content_css = ('<link type="text/css" href="/static/reset.css" />' +
                                '<link type="text/css" href="/static/common.css" />')

        context = Context()
        template = Template(tpl)
        output = template.render(context)

        # TODO: more strict checks to see if the tags are really at bottom
        self.assertTrue(expected_content_js in output, msg='script tags are collected and rendered at bottom')
        self.assertTrue(expected_content_css in output, msg='style tags are collected and rendered at bottom')

    #TODO: get_assets should populate context, not output!

    #TODO: exceptions test

    #TODO: empty {% collect_assets js %}{% endcollect_assets %} is redundant, yet necessary