from Core.models import Rating

class UserUserCollabManager:

	def __init__(self, user, item):
		self.user = user
		self.item = item

	def predict(self):
		if Rating.standardDeviation(self.user): # i.e., can give Personalised recommendations
			print ("User's Standard Deviation is not 0 => Can give Personalised Recommendation")
			# term1: \frac { \sum \limits_{u \in Users - \{a\}} z_{u,i} * sim(a,u) } { \sum \limits_{u \in Users - \{a\}} | sim(a,u) | }
			term1 = self._calcTerm1()
			if term1 is not None: # term1 will be None if no user (leaving out the one under consideration) has rated the item under consideration
				prediction = ( (term1) * Rating.standardDeviation(self.user) ) + Rating.mean(self.user)
			else:
				return None
			return prediction
		else:
			return self.getNonPersonlisedPrediction()

	def _calcTerm1(self):
		# term1: \frac { \sum \limits_{u \in Users - \{a\}} z_{u,i} * sim(a,u) } { \sum \limits_{u \in Users - \{a\}} | sim(a,u) | }
		numerator = denominator = 0

		for user in Rating.getUsersWhoHaveRated_item(self.item):
			if user != self.user:
				similarity = self._getSimilarity(user)
				print ("Similarity between", self.user.pk , "and", user.pk, "is", similarity)
				print ("Z-Score of", user.pk , "is", self._getZScore(user))

				numerator += self._getZScore(user) * similarity

				denominator += abs(similarity)

		# If there were users (leaving out the one under consideration) who rated the item and ALL their similarities were not 0
		if denominator is not 0:
			return numerator/denominator
		else:
			return None

	def _getZScore(self, user):
		# \frac { r_{u,i} - \mu_u } { \sigma_u }
		
		numerator = Rating.objects.get(user=user, item=self.item).rating - Rating.mean(user)
		denominator = Rating.standardDeviation(user)

		if denominator is not 0:
			return numerator/denominator
		else:
			return 0 # refer documenation for justification

	# This implements the Pearson Correlation Coefficient
	# \frac { \sum \limits_{i \in Common Items} ( r_{a,i} - \mu_a ) ( r_{u,i} - \mu_u ) } { \sigma_a \sigma_u }
	def _getSimilarity(self, user):
		if not Rating.standardDeviation(self.user):
			raise ValueError('Standard Deviation of User under consideration is 0. Personalised recommendation not possible')

		if Rating.standardDeviation(user):
			similarity = 0
			for item in set.intersection(set(Rating.getItemsWhichHaveBeenRated_user(self.user)), set(Rating.getItemsWhichHaveBeenRated_user(user))):
				similarity += ( (Rating.objects.get(user=self.user, item=item).rating - Rating.mean(self.user)) * (Rating.objects.get(user=user, item=item).rating - Rating.mean(user)) )

			similarity /= (Rating.standardDeviation(self.user) * Rating.standardDeviation(user))

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
