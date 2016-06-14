from translator.models import Language
from rest_framework import serializers

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Language
		fields = ('ko', 'en')

	
