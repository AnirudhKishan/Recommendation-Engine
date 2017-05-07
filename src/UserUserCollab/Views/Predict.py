import os, json

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from Lib.enum import Enum
from Core.models import User, Item, Rating
from UserUserCollab.Lib import UserUserCollabManager


def predict(request, userId, itemId):

	config = json.load(open(os.path.dirname(os.path.abspath(__file__))+'/Predict_config.json'))

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
	
	prediction = UserUserCollabManager(user=user, item=item).predict()

	if prediction is None:
		resp = {
			'status': config['error']['cannotPredict']['code'],
			'msg': config['error']['cannotPredict']['msg'],
		}
		return HttpResponse(json.dumps(resp), content_type='application/json')

	resp = {
	'status': 0,
	'prediction': prediction,
	}

	if Rating.objects.filter(user=user, item=item):
		resp.update({
			'rating': Rating.objects.get(user=user, item=item).rating,
		})
	return HttpResponse(json.dumps(resp), content_type='application/json')
