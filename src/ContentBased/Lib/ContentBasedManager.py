from Core.models import Rating, Attribute, ItemAttribute

class ContentBasedManager:

	def __init__(self, user, item):
		self.user = user
		self.item = item
		self._userVector = {}

	def predict(self):
		self._getUserVector()
		
		print("The user vector is:")
		print(self._userVector)

		cosineDistance = self._getCosineDistance()
		print("The cosine distance is", cosineDistance)

		# convert cosine distance to n-point rating
		rating = 5 * cosineDistance
		print("5-point scale rating :", rating)

		# mean centering rating
		rating = (rating-2.5) + Rating.mean(self.user)
		print("Mean-Cantered rating :", rating)

		return rating

	def _getUserVector(self):
		# teh below for loops(s) seem to have bloat
		for item in Rating.getItemsWhichHaveBeenRated_user(self.user):
			for attribute in Attribute.objects.all():
				# finding out weight of attribute wrt. item:
				if ItemAttribute.objects.filter(item=item, attribute=attribute).exists():
					weight = 1
				else:
					weight = 0

				try:
					self._userVector[attribute.pk] += weight * Rating.objects.get(user=self.user, item=item).rating
				except KeyError:
					self._userVector[attribute.pk] = weight * Rating.objects.get(user=self.user, item=item).rating

	def _getCosineDistance(self):

		itemVector =  self.item.getItemAttributes()
		print("The item vector is:")
		print(itemVector)

		# To Be Refactored: as "Dot Product"
		output = 0
		for attribute in Attribute.objects.all():
			output += self._userVector[attribute.pk] * itemVector[attribute.pk]

		# To Be Refactored: as "Vector Magnitude"
		magnitude_itemVector = 0
		for key, val in itemVector.items():
			magnitude_itemVector += val**2
		magnitude_itemVector =  magnitude_itemVector**(0.5)
		print("magnitude of itemVector ", magnitude_itemVector)
		magnitude_userVector = 0
		for key, val in self._userVector.items():
			magnitude_userVector += val**2
		magnitude_userVector =  magnitude_userVector**(0.5)
		print("magnitude of userVector ", magnitude_userVector)


		return (output/(magnitude_userVector*magnitude_itemVector))
