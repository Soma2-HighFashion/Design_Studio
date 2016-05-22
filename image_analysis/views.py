# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
from subprocess import Popen, PIPE, STDOUT

import numpy as np
import tflearn as tl
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.data import generate_patches, img2numpy_arr

# Create your views here.
def classify_gender(request):
	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"

	X = generate_patches(img2numpy_arr(design_path + input_image_uid))

	model = construct_model(2)
	image_analysis_path = "/home/dj/HighFashionProject/design_studio/image_analysis/"
	model.load(image_analysis_path + 'vgg_gender_model-80000')
	pred_y = model.predict(X)

	return JsonResponse(
		{'results' : pred_y}
	)

def classify_category(request):
	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"

	X = generate_patches(img2numpy_arr(design_path + input_image_uid))

	model = construct_model(6)
	image_analysis_path = "/home/dj/HighFashionProject/design_studio/image_analysis/"
	model.load(image_analysis_path + 'vgg_category_model-130000')
	pred_y = model.predict(X)

	return JsonResponse(
		{'results' : pred_y}
	)

def construct_model(num_classes):
	# Building 'VGG Network'
	network = input_data(shape=[None, 84, 84, 3])

	network = conv_2d(network, 64, 3, activation='relu')
	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 128, 3, activation='relu')
	network = conv_2d(network, 128, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 256, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 512, 3, activation='relu')
	network = conv_2d(network, 512, 3, activation='relu')
	network = conv_2d(network, 512, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 512, 3, activation='relu')
	network = conv_2d(network, 512, 3, activation='relu')
	network = conv_2d(network, 512, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = fully_connected(network, 4096, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, num_classes, activation='softmax')

	network = regression(network, optimizer='rmsprop',
						 loss='categorical_crossentropy',
						 learning_rate=0.00001)
	# Model
	model = tl.DNN(network)
	return model


