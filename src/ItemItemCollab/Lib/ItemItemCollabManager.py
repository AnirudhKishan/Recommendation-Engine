from Core.models import Rating

class ItemItemCollabManager:

	def __init__(self, user, item):
		self.user = user
		self.item = item

	def predict(self):
		if Rating.standardDeviation(self.item): # i.e., can give Personalised recommendations
			print ("Item's Standard Deviation is not 0 => Can give Personalised Recommendation")
			# term1: \frac { \sum \limits_{i \in Items - \{a\}} z_{u,i} * sim(a,i) } { \sum \limits_{i \in Items - \{a\}} | sim(a,i) | }
			term1 = self._calcTerm1()
			if term1 is not None: # term1 will be None if no user (leaving out the one under consideration) has rated the item under consideration OR the similarirites of all the users who have rated the item against the user under consideration is 0
				prediction = ( (term1) * Rating.standardDeviation(self.item) ) + Rating.mean(self.item)
			else:
				return None
			return prediction
		else:
			return self.getNonPersonlisedPrediction()

	def _calcTerm1(self):
		# term1: \frac { \sum \limits_{i \in Items - \{a\}} z_{u,i} * sim(a,i) } { \sum \limits_{i \in Items - \{a\}} | sim(a,i) | }
		numerator = denominator = 0

		for item in Rating.getItemsWhichHaveBeenRated_user(self.user):
			if item != self.item:
				similarity = self._getSimilarity(item)
				print ("Similarity between", self.item.pk , "and", item.pk, "is", similarity)
				print ("Z-Score of", item.pk , "is", self._getZScore(item))

				numerator += self._getZScore(item) * similarity

				denominator += abs(similarity)

		# If there were users (leaving out the one under consideration) who rated the item and ALL their similarities were not 0
		if denominator is not 0:
			return numerator/denominator
		else:
			return None

	def _getZScore(self, item):
		# \frac { r_{u,i} - \mu_u } { \sigma_u }
		
		numerator = Rating.objects.get(user=self.user, item=item).rating - Rating.mean(item)
		denominator = Rating.standardDeviation(item)

		if denominator is not 0:
			return numerator/denominator
		else:
			return 0 # refer documenation for justification

	# This implements the Pearson Correlation Coefficient
	# \frac { \sum \limits_{i \in Common Items} ( r_{a,i} - \mu_a ) ( r_{u,i} - \mu_u ) } { \sigma_a \sigma_u }
	def _getSimilarity(self, item):
		if not Rating.standardDeviation(self.item):
			raise ValueError('Standard Deviation of Item under consideration is 0. Personalised recommendation not possible')

		if Rating.standardDeviation(item):
			similarity = 0
			for user in set.intersection(set(Rating.getUsersWhoHaveRated_item(self.item)), set(Rating.getUsersWhoHaveRated_item(item))):
				similarity += ( (Rating.objects.get(user=user, item=self.item).rating - Rating.mean(self.item)) * (Rating.objects.get(user=user, item=item).rating - Rating.mean(item)) )

			similarity /= (Rating.standardDeviation(self.item) * Rating.standardDeviation(item))

			return similarity
		else:
			return 0 # refer documenation for justification

	def getNonPersonlisedPrediction(self):
		# \frac { \sum \limits_{u \in Users - \{a\}} r_{u, i} } { n }

		numerator = denominator = 0
		for user in Rating.getUsersWhoHaveRated_item(self.item):
			if user != self.user:
				numerator += Rating.objects.get(user=user, item=self.item).rating
				denominator += 1

		if denominator is not 0:
			return numerator/denominator
		else:
			return None
