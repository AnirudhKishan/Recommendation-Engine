from django.db import models
from Lib import Statistics

from .User import User
from .Item import Item

class Rating(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item)

	rating = models.PositiveSmallIntegerField()

	class Meta:
		app_label = 'Core'
		unique_together = ('user', 'item')

	@staticmethod
	def getUsersWhoHaveRated_item(item):
		ratings_item = Rating.objects.filter(item=item)

		result = []
		for each in ratings_item:
			result.append(each.user)

		return result

	@staticmethod
	def getItemsWhichHaveBeenRated_user(user):
		ratings_user = Rating.objects.filter(user=user)

		result = []
		for each in ratings_user:
			result.append(each.item)

		return result

	@classmethod
	def standardDeviation(cls, arg=None):
		if arg is None:
			return cls._standardDeviation()
		elif type(arg) is User:
			return cls._standardDeviation_user(arg)
		elif type(arg) is Item:
			return cls._standardDeviation_item(arg)
		else:
			raise TypeError

	@staticmethod
	def _standardDeviation():
		ratings = [x.rating for x in Rating.objects.all()]
		return Statistics.stdDev(ratings)

	@staticmethod
	def _standardDeviation_user(user):
		ratings = [x.rating for x in Rating.objects.filter(user=user)]
		return Statistics.stdDev(ratings)

	@staticmethod
	def _standardDeviation_item(item):
		ratings = [x.rating for x in Rating.objects.filter(item=item)]
		return Statistics.stdDev(ratings)

	@classmethod
	def mean(cls, arg=None):
		if arg is None:
			return cls._mean()
		elif type(arg) is User:
			return cls._mean_user(arg)
		elif type(arg) is Item:
			return cls._mean_item(arg)
		else:
			raise TypeError

	@staticmethod
	def _mean():
		ratings = [x.rating for x in Rating.objects.all()]
		return Statistics.mean(ratings)

	@staticmethod
	def _mean_user(user):
		ratings = [x.rating for x in Rating.objects.filter(user=user)]
		return Statistics.mean(ratings)

	@staticmethod
	def _mean_item(item):
		ratings = [x.rating for x in Rating.objects.filter(item=item)]
		return Statistics.mean(ratings)
