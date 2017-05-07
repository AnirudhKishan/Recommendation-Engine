import os, json

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from Lib.enum import Enum
from Core.models import User, Item, Rating
from ItemItemCollab.Lib import ItemItemCollabManager
from UserUserCollab.Lib import UserUserCollabManager
from ContentBased.Lib import ContentBasedManager


def predict(request, userId, itemId, w1=None, w2=None, w3=None):

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
	
	if (w1 == None):
		prediction = (UserUserCollabManager(user=user, item=item).predict() + ItemItemCollabManager(user=user, item=item).predict() + ContentBasedManager(user=user, item=item).predict()) / 3
	else:
		prediction = (UserUserCollabManager(user=user, item=item).predict() * float(w1) + ItemItemCollabManager(user=user, item=item).predict() * float(w2) + ContentBasedManager(user=user, item=item).predict() * float(w3)) / (float(w1)+float(w2)+float(w3))
	
	print("")
	print("Hybrid Prediction:",prediction)

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
