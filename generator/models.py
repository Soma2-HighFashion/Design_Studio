from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# Create your models here.
@python_2_unicode_compatible
class Image(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200)
	gender = models.CharField(max_length=100)
	category = models.CharField(max_length=150)
	uid = models.CharField(max_length=50)
	history = models.CharField(max_length=100)
	filterd = models.BooleanField()
	like = models.IntegerField()

	def __str__(self):
		return '%s' % (self.text)
