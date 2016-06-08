from generator.models import Image, Design
from rest_framework import serializers

class ImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Image
		fields = ('uid', 'text', 'gender', 'category')

class DesignSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Design
		fields = ('uid', 'history_uid', 'history_text', 'filterd', 'like')

		
