from django.conf.urls import patterns, url

from .Views import predict, weighted


urlpatterns = patterns ('',
	url(r'^(?P<userId>\d+)/(?P<itemId>\d+)$', predict, name='predict'),
	url(r'^(?P<userId>\d+)/(?P<itemId>\d+)/(?P<w1>\d+)/(?P<w2>\d+)/(?P<w3>\d+)$', predict, name='predictWeights'),
	url(r'^weighted$', weighted, name='weighted'),
	)
