from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="form.html")),
    url(r'^kbsearch/(?P<id>\w+)/$', views.search_kb, name='searchkb'),    
    url(r'^getpage/$', views.get_page, name='getpage'),    
    url(r'^search_extracted/(?P<id>\w+)/$', views.search_extracted, name='search_extracted'),     
]

