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

from generator.models import Design
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
	designs = Design.objects.all()

	image_list = []
	history_list = []
	for design in designs:
		image_list.append(str(design.uid) + ".png")
		history_list.append(str(design.history_text))

	d_geometry = settings.D_GEOMETRY
	designed_images = np.empty((len(image_list), d_geometry[0]*d_geometry[1]*3), dtype="float32")
	for i in range(len(image_list)):
		designed_images[i] = img2numpy_arr(settings.DESIGN_PATH + image_list[i]).reshape(d_geometry[0]*d_geometry[1]*3)
	designed_images /= 255
	
	lshf = LSHForest(random_state=42)
	lshf.fit(designed_images) 

	num = int(request.GET['num'])
	input_fname = str(request.GET['input'])
	input_image = img2numpy_arr(settings.DESIGN_PATH + input_fname)
	input_image = input_image.reshape(1, -1)/255
	_, indices = lshf.kneighbors(input_image, n_neighbors=num)

	similar_images = []
	for i in list(indices.reshape(-1)):
		similar_images.append({ "image": image_list[i], "text": history_list[i] })

	return JsonResponse({
		"results": similar_images
	})

	
