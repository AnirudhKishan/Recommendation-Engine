from django.db import models

class User(models.Model):
	username = models.CharField(max_length=255, unique=True)

	class Meta:	app_label = 'Core'