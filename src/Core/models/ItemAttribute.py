from django.db import models

from .Item import Item
from .Attribute import Attribute


class ItemAttribute(models.Model):
	item = models.ForeignKey(Item)
	attribute = models.ForeignKey(Attribute)

	class Meta:	app_label = 'Core'
