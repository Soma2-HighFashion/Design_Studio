import requests
import urllib
import re 

import numpy as np
from gensim.models import Word2Vec
from nltk.corpus import stopwords

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def translate(input_text):
	naver_api = "https://openapi.naver.com/v1/language/translate"
	client_id = settings.CLIENT_ID
	client_secret = settings.CLIENT_SECRET

	headers = {
		'X-Naver-Client-Id': client_id,
		'X-Naver-Client-Secret': client_secret
	}
	
	params = {
		'source': 'ko',
		'target': 'en',
		'text': input_text.encode('utf-8')
	}
	
	r = requests.post(naver_api, data=params, headers=headers)

	try:
		translated_text = r.json()['message']['result']['translatedText']
	except:
		translated_text = "Random"

	return translated_text

if not settings.DEBUG:
	print("Load Word2Vec Pre-trained model")
	w2v_model = Word2Vec.load_word2vec_format(
			settings.WORD2VEC_PATH + 'pre-trained/GoogleNews-vectors-negative300.bin.gz', binary=True)
	print("Load Complete!")

def analysis_word2vec(input_text):
	clean_list = text_to_word(input_text)
	print "Clean List:", clean_list
	
	female = "female"; male = "male"
	street = "hiphop"; casual = "casual"
	classic = "suit"; unique = "unique"
	sexy = "sexy"

	f_score = 0; m_score = 0
	str_score = 0; cas_score = 0
	cla_score = 0; uni_score = 0
	sexy_score = 0

	weight = 50
	for word in clean_list:
		f_score += w2v_model.similarity(word, female) * weight
		m_score += w2v_model.similarity(word, male) * weight
		
		str_score += w2v_model.similarity(word, street) * weight
		cas_score += w2v_model.similarity(word, casual) * weight
		cla_score += w2v_model.similarity(word, classic) * weight
		uni_score += w2v_model.similarity(word, unique) * weight
		sexy_score += w2v_model.similarity(word, sexy) * weight

	gender_list = [f_score, m_score]
	category_list = [
		str_score, cas_score, cla_score, uni_score, sexy_score
	]

	return softmax(gender_list), softmax(category_list)

def text_to_word(text):
	text = text.replace("-", "")
	text = re.sub("[^a-zA-Z]", " ", text)
	text = text.lower().split()

	stops = set(stopwords.words("english"))

	clean_text = [w for w in text if not w in stops]
	return clean_text

def softmax(input_list):
	nparr = np.array(input_list)
	e = np.exp(nparr)
	prob = e / np.sum(e)
	return prob

