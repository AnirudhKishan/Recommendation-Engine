from django.conf.urls import patterns, url

from .Views import predict


urlpatterns = patterns ('',
	url(r'^(?P<userId>\d+)/(?P<itemId>\d+)$', predict, name='predict'),
	)
