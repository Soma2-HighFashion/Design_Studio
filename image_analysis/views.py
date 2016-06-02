# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import time
import json
from subprocess import Popen, PIPE, STDOUT

import numpy as np
from sklearn.neighbors import LSHForest

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.data import generate_patches, img2numpy_arr

# Create your views here.
def classify_discriminator(image_fname):
	os.chdir(settings.IMAGE_ANALYSIS_PATH)

	cmd = ("python test_discriminate.py --t " + settings.GENERATOR_PATH + image_fname)
	classify_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	pred_y = classify_image.stdout.read()

	start_index = pred_y.index('[[')
	end_index = pred_y.index(']]') + 2
	return json.loads(pred_y[start_index:end_index])

def classify_fashion(image_fname):
	os.chdir(settings.IMAGE_ANALYSIS_PATH)

	cmd = ("python test_analysis.py --t "+ settings.GENERATOR_PATH + image_fname)
	classify_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	pred_y = classify_image.stdout.read()

	start_index = pred_y.index("[[")
	end_index = pred_y.index("]]") + 2
	return json.loads(pred_y[start_index:end_index])

def search_neighbors(request):
	image_list = os.listdir(settings.DESIGN_PATH)

	d_geometry = settings.D_GEOMETRY
	train_X = np.empty((len(image_list), d_geometry[0]*d_geometry[1]*3), dtype="float32")
	for i in range(len(image_list)):
		train_X[i] = img2numpy_arr(desinged_path + image_list[i]).reshape(d_geometry[0]*d_geometry[1]*3)
	train_X /= 255
	
	lshf = LSHForest(random_state=42)
	lshf.fit(train_X) 

	num = int(request.GET['num'])
	test_fname = str(request.GET['input'])
	test_X = img2numpy_arr(settings.DESIGN_PATH + test_fname)
	test_X = test_X.reshape(1, -1)/255
	_, indices = lshf.kneighbors(test_X, n_neighbors=num)

	return JsonResponse({
		"results": indices
	})

	
