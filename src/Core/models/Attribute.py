from django.db import models

class Attribute(models.Model):
	name = models.CharField(max_length=255, unique=True)

	class Meta:	app_label = 'Core'