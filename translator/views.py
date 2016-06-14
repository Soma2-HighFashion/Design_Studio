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
	
	try:
		r = requests.post(naver_api, data=params, headers=headers)
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

	for word in clean_list:
		f_score += (w2v_model.similarity(word, female) * settings.GENDER_WEIGHT)
		m_score += (w2v_model.similarity(word, male) * settings.GENDER_WEIGHT)
		
		str_score += w2v_model.similarity(word, street) 
		cas_score += w2v_model.similarity(word, casual) 
		cla_score += w2v_model.similarity(word, classic) 
		uni_score += w2v_model.similarity(word, unique) 
		sexy_score += w2v_model.similarity(word, sexy) 

	gender_list = [f_score, m_score]
	category_list = [
		str_score, cas_score, cla_score, uni_score, sexy_score
	]

	gender_list = softmax(gender_list)
	category_list = map(lambda x: x/float(sum(category_list)), category_list)
	
	return gender_list, category_list

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

