# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import time
import json
from subprocess import Popen, PIPE, STDOUT

import numpy as np
from sklearn.neighbors import LSHForest

from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.data import generate_patches, img2numpy_arr

# Create your views here.
def classify_discriminator(image_fname):
	image_analysis_path = "/home/dj/HighFashionProject/image_analysis/"
	os.chdir(image_analysis_path)

	generator_path = "/home/dj/HighFashionProject/design_studio/static_files/generator/"

	cmd = ("python test_discriminate.py --t "+ generator_path + image_fname)
	classify_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	pred_y = classify_image.stdout.read()

	start_index = pred_y.index('[[')
	end_index = pred_y.index(']]') + 2
	return json.loads(pred_y[start_index:end_index])

def classify_fashion(request):
	image_analysis_path = "/home/dj/HighFashionProject/image_analysis/"
	os.chdir(image_analysis_path)

	generator_path = "/home/dj/HighFashionProject/design_studio/static_files/generator/"
	input_image_uid = str(request.GET['input'])

	cmd = ("python test_analysis.py --t "+ generator_path + input_image_uid)
	classify_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	pred_y = classify_image.stdout.read()

	start_index = pred_y.index("[[")
	end_index = pred_y.index("]]") + 2
	return JsonResponse({ "results": json.loads(pred_y[start_index:end_index]) })

def search_neighbors(request):
	desinged_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"	
	image_list = os.listdir(desinged_path)

	train_X = np.empty((len(image_list), 256*84*3), dtype="float32")
	for i in range(len(image_list)):
		train_X[i] = img2numpy_arr(desinged_path + image_list[i]).reshape(256*84*3)
	train_X /= 255
	
	lshf = LSHForest(random_state=42)
	lshf.fit(train_X) 

	num = int(request.GET['num'])
	test_fname = str(request.GET['input'])
	test_X = img2numpy_arr(desinged_path + test_fname)
	test_X = test_X.reshape(1, -1)/255
	_, indices = lshf.kneighbors(test_X, n_neighbors=num)

	return JsonResponse({
			"results": indices
			})

	
