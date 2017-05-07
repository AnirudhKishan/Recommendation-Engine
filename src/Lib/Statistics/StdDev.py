import math

from .Mean import mean

def stdDev(list):
	if list:
		variance = 0
		for each in list:
			variance += (each - mean(list)) ** 2
		variance /= len(list)

		return math.sqrt(variance)
	else:
		return None