import requests
import urllib

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def translate(request):
	naver_api = "https://openapi.naver.com/v1/language/translate"
	client_id = "mInBhy5qJvHGe4olYpq0"
	client_secret = "vSB7DszOPY"

	headers = {
		'X-Naver-Client-Id': client_id,
		'X-Naver-Client-Secret': client_secret
	}
	
	request.GET['text']
	input_text = urllib.unquote(request.GET['text'])
	print(input_text)
	params = {
		'source': 'ko',
		'target': 'en',
		'text': input_text.encode('utf-8')
	}
	
	r = requests.post(naver_api, data=params, headers=headers)

	return JsonResponse(
		{'results' : r.text}
	)

