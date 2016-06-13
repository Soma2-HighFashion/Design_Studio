from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# Create your models here.
@python_2_unicode_compatible
class Image(models.Model):
	uid = models.CharField(primary_key=True, max_length=50)
	text = models.CharField(max_length=200)
	gender = models.CharField(max_length=100)
	category = models.CharField(max_length=150)

	def __str__(self):
		return '%s' % (self.text)

class Design(models.Model):
	uid = models.CharField(primary_key=True, max_length=50)
	history_uid = models.CharField(max_length=500)
	history_text = models.CharField(max_length=300)
	filterd = models.BooleanField()
	like = models.IntegerField()

	def __str__(self):
		return '%s' % ("Design" + self.uid)


