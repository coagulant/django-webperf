from django.conf.urls.defaults import patterns
from django.http import HttpResponse
from django.template.base import Template
from django.template.response import SimpleTemplateResponse, TemplateResponse

def index_view(request):
    return TemplateResponse(request, Template('test'))
#    return HttpResponse('')

urlpatterns = patterns('',
    ('^$', index_view)
    )