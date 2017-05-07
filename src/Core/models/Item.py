from django.db import models

from .Attribute import Attribute


class Item(models.Model):
	name = models.CharField(max_length=255, unique=True)

	def getItemAttributes(self):
		from .ItemAttribute import ItemAttribute
		itemAttributes = {}
		for attribute in Attribute.objects.all():
			# finding out weight of attribute wrt. item:
			if ItemAttribute.objects.filter(item=self, attribute=attribute).exists():
				weight = 1
			else:
				weight = 0
			itemAttributes[attribute.pk] = weight
		return itemAttributes

	class Meta:	app_label = 'Core'