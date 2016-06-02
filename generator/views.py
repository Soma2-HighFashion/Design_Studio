import os
import time
from subprocess import Popen, PIPE, STDOUT
import uuid
import urllib

from PIL import Image
import numpy as np

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.views import classify_discriminator, classify_fashion 
from translator.views import translate, analysis_word2vec

# Create your views here.
def generator(request):
	input_text = urllib.unquote(request.GET['text'])
	translated_text = translate(input_text)

	os.chdir(settings.DCGAN_PATH)
	image_uid = str(uuid.uuid4())

	# Generate Random Image
	f_name = generate_random_image(image_uid)

	#  Classify Generate Image - Good or Bad
	pred_y = classify_discriminator(f_name)
	good_img_list = classify_good_generated(pred_y)
	
	#  Find Best Image with Word2Vec  - Gender and Category

	pred_fashion = classify_fashion(f_name)
	best_index = find_best_image(good_img_list, pred_fashion, analysis_word2vec(translated_text))

	# Crop Best Image
	crop_image_and_save(best_index, f_name)

	return JsonResponse(
		{'results' : f_name}
	)

def generate_random_image(image_uid):
	cmd = ("gpu=0 noise=normal name="+image_uid+ " batchSize=" + str(settings.G_COUNT) +
			" net=checkpoints/fashionG_18_net_G.t7 th generate.lua")
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

def find_best_image(good_img_list, pred_fashion, analysis_word2vec):
	gender_classifier, category_classifier = analysis_word2vec

	print "classifier Gender:", gender_classifier
	print "classifier Category:,", category_classifier

	f_patch_count = settings.F_PATCH_COUNT
	best_image_index = 0
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
				street_count/f_patch_count, casual_count/f_patch_count,
				classic_count/f_patch_count, unique_count/f_patch_count,
				sexy_count/f_patch_count
				], dtype="float32")

		print "No.", i, "pred Gender:", pred_gender
		print "No.", i, "pred Category:", pred_category

		diff = get_dist(gender_classifier, pred_gender) + get_dist(category_classifier, pred_category)

		print "diff:", diff

		if diff < best_diff:
			best_image_index = i
			best_diff = diff

	return best_image_index

def get_dist(x, y):
	return np.sqrt(np.sum((x-y)**2))

def crop_image_and_save(index, f_name):
	generator_path = settings.GENERATOR_PATH
	input_image = Image.open(generator_path + f_name)

	g_geometry = settings.G_GEOMETRY
	y,x = divmod(index, settings.G_IMAGE[1])
	left = x * g_geometry[1]
	right = (x+1) * g_geometry[1]
	top = y * g_geometry[0]
	bottom = (y+1) * g_geometry[0]

	best_image = input_image.crop((left, top, right, bottom)).save(generator_path+f_name)
