from generator.models import Image
from rest_framework import serializers

class ImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Image
		fields = ('id', 'text', 'gender', 'category', 'uid', 'history', 'filterd', 'like')

		
