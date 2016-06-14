# -*- coding: utf-8 -*-

import os
import time
from subprocess import Popen, PIPE, STDOUT
import uuid
import urllib
import json

from PIL import Image as PILImage
import numpy as np

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from generator.forms import UploadFileForm
from rest_framework import viewsets, renderers, filters

from generator.models import Image, Design
from translator.models import Language
from generator.serializer import ImageSerializer, DesignSerializer
from image_analysis.views import classify_discriminator, classify_fashion 
from translator.views import translate, analysis_word2vec

# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('uid', 'text', 'gender', 'category')

	queryset = Image.objects.all()
	serializer_class = ImageSerializer

class DesignViewSet(viewsets.ModelViewSet):
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('uid', 'history_uid', 'history_text', 'filtered', 'like')

	queryset = Design.objects.all()
	serializer_class = DesignSerializer

def all_word(request):
	return JsonResponse({
		'results' : map(lambda x: urllib.unquote(x).decode('utf8'), word_list())
	})

def word_list():
	designs = Design.objects.all()
	text_list = []
	for design in designs:
		plus_urlencode = "%20%2B%20"; underbar_urlencode = "%20_%20"
		text = str(design.history_text).replace(plus_urlencode,' ').replace(underbar_urlencode,' ')
		text_list += text.split()
	return list(set(text_list))

def designs_contain_word(request):
	designs = Design.objects.all()
	word = request.GET['word']
	
	image_list = []
	history_list = []
	like_list = []
	for design in designs:
		image_list.append(str(design.uid) + ".png")
		history_list.append(str(design.history_text))
		like_list.append(int(design.like))

	history_list = map(lambda x: urllib.unquote(x).decode('utf8'), history_list)
	contain_list = filter(lambda x: word in x[1], zip(image_list, history_list, like_list))
	contain_list = map(lambda x: {"image": x[0], "text": x[1], "like": x[2]}, contain_list)
	return JsonResponse({
		"results": contain_list
	})

def test(request):
	form = UploadFileForm(request.POST, request.FILES)
	filtered_image = False
	if form.is_valid():
		filtered_image = request.FILES['file']
	return JsonResponse({"results": filtered_image}) 

def top10(request):
	top10_list = []
	designs = Design.objects.order_by('like').reverse()
	for design in designs[:10]:
		top10_list.append({
			'image': design.uid,
			'text': urllib.unquote(str(design.history_text)),
			'history': design.history_uid,
			'filtered': design.filtered,
			'like': design.like
		});
	return JsonResponse({
		"results": top10_list
	})

def generator(request):
	is_arithmetic = json.loads(request.GET['arithmetic'])
	input_text = request.GET['text']

	os.chdir(settings.DCGAN_PATH)
	image_uid = str(uuid.uuid4())

	# Generate Random Image
	f_name = generate_random_image(image_uid)

	#  Classify Generate Image - Good or Bad
	pred_y = classify_discriminator(f_name)
	good_img_list = classify_good_generated(pred_y)
	
	#  Find Best Image with Word2Vec  - Gender and Category

	pred_fashion = classify_fashion(f_name)
	
	if settings.DEBUG:
		translated_text = ""
		best_index, gender, category = find_best_image(good_img_list, pred_fashion)
	else:
		if (is_arithmetic):
			translated_text = urllib.unquote(input_text)
			print("arithmetic")
		else:
			if Language.objects.filter(ko=input_text).exists():
				print("exist")
				translated_text = str(Language.objects.filter(ko=input_text)[0].en)
			else:
				print("no exist")
				translated_text = translate(urllib.unquote(input_text))
				if translated_text != "Random":
					Language(ko=input_text, en=translated_text).save()
		best_index, gender, category = find_best_image(
				good_img_list, pred_fashion, analysis_word2vec(translated_text))

	# Crop Best Image
	crop_image_and_save(best_index, f_name)

	return JsonResponse({
		'results' : f_name,
		'gender' : list(gender),
		'category' : list(category)
	})

def generate_random_image(image_uid):
	cmd = ("gpu=0 noise=normal name="+image_uid+ " batchSize=" + str(settings.G_COUNT) +
			" net=checkpoints/fashionG_18_net_G.t7 " + settings.TORCH_PATH + "th generate.lua")
	generate_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	return os.path.basename(generate_image.stdout.read()).strip()
	
def classify_good_generated(pred_y):
	image_count = settings.G_COUNT
	d_patch_count = settings.D_PATCH_COUNT

	good_img_list = []
	threshold = 0.7
	for i in range(image_count):
		good_count = 0
		for j in range(i*d_patch_count, (i+1)*d_patch_count):
			good_count += pred_y[j][1]
		eval_d = good_count/d_patch_count
		print "No.", (i+1), " Discriminator Result:", eval_d
		if eval_d >= threshold:
			good_img_list.append(i)
	print good_img_list
	return good_img_list	

def find_best_image(good_img_list, pred_fashion, 
					analysis_word2vec=(np.array([0,0]), np.array([0,0,0,0,0]))):
	gender_classifier, category_classifier = analysis_word2vec

	print "classifier Gender:", gender_classifier
	print "classifier Category:,", category_classifier

	is_category_focused = False
	if max(category_classifier) > settings.CATEGORY_THRESHOLD:
		is_category_focused = True

	f_patch_count = settings.F_PATCH_COUNT
	best_image_index = 0
	best_image_gender = 0
	best_image_category = 0
	best_diff = 1000

	for i in good_img_list:
		female_count = 0; male_count = 0;
		street_count = 0; casual_count = 0; classic_count = 0; 
		unique_count = 0; sexy_count = 0;

		for j in range(i*f_patch_count, (i+1)*f_patch_count):
			female_count += sum(pred_fashion[j][0:5])
			male_count += sum(pred_fashion[j][5:])

			street_count += (pred_fashion[j][0] + pred_fashion[j][5])
			casual_count += (pred_fashion[j][1] + pred_fashion[j][6])
			classic_count += (pred_fashion[j][2] + pred_fashion[j][7])
			unique_count += (pred_fashion[j][3] + pred_fashion[j][8])
			sexy_count += pred_fashion[j][4]

		pred_gender = np.array([
				female_count/f_patch_count, male_count/f_patch_count
				], dtype="float32")

		pred_category = np.array([
				street_count*settings.STREET_WEIGHT / f_patch_count, 
				casual_count*settings.CASUAL_WEIGHT / f_patch_count,
				classic_count*settings.CLASSIC_WEIGHT / f_patch_count, 
				unique_count*settings.UNIQUE_WEIGHT / f_patch_count,
				sexy_count*settings.SEXY_WEIGHT / f_patch_count
				], dtype="float32")
		pred_category /= sum(pred_category)

		print "No.", i, "pred Gender:", pred_gender
		print "No.", i, "pred Category:", pred_category

		if is_category_focused:
			category_index = category_classifier.index(max(category_classifier))
			diff = 1 - pred_category[category_index]
		else:
			diff = (euclidean(gender_classifier, pred_gender) + 
					euclidean(category_classifier, pred_category))

		print "diff:", diff

		if diff < best_diff:
			best_image_index = i
			best_image_gender = pred_gender
			best_image_category = pred_category
			best_diff = diff

	best_image_gender = map(lambda x: round(x, 3), list(best_image_gender))
	best_image_category = map(lambda x: round(x, 3), list(best_image_category))

	return best_image_index, best_image_gender, best_image_category

def softmax(x):
	return np.exp(x)/sum(np.exp(x))

def euclidean(x, y):
	return np.sqrt(np.sum((x-y)**2))

def crop_image_and_save(index, f_name):
	generator_path = settings.GENERATOR_PATH
	input_image = PILImage.open(generator_path + f_name)

	g_geometry = settings.G_GEOMETRY
	y,x = divmod(index, settings.G_IMAGE[1])
	left = x * g_geometry[1]
	right = (x+1) * g_geometry[1]
	top = y * g_geometry[0]
	bottom = (y+1) * g_geometry[0]

	best_image = input_image.crop((left, top, right, bottom)).save(generator_path+f_name)
