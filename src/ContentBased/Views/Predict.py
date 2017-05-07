import json

from django.http import HttpResponse

from Lib.enum import Enum
from Core.models import User, Item, Rating
from ContentBased.Lib import ContentBasedManager


def predict(request, userId, itemId):
	try:
		user = User.objects.get(pk=userId)
	except ObjectDoesNotExist:
		resp = {
			'status': config['error']['invalidUserId']['code'],
			'msg': config['error']['invalidUserId']['msg'],
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')


	try:
		item = Item.objects.get(pk=itemId)
	except ObjectDoesNotExist:
		resp = {
			'status': config['error']['invalidItemId']['code'],
			'msg': config['error']['invalidItemId']['msg'],
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')

	a = ContentBasedManager(user, item)
	prediction = a.predict()
	
	resp = {
	'status': 0,
	'prediction': prediction,
	}

	if Rating.objects.filter(user=user, item=item):
		resp.update({
			'rating': Rating.objects.get(user=user, item=item).rating,
		})
	return HttpResponse(json.dumps(resp), content_type='application/json')

	return HttpResponse(str(prediction))
