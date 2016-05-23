# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import time
from subprocess import Popen, PIPE, STDOUT

import numpy as np
import tflearn as tl
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.data import generate_patches, img2numpy_arr

def construct_network():
	tl.init_graph(num_cores=8, gpu_memory_fraction=0.4)

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

#image_analysis_path = "/home/dj/HighFashionProject/design_studio/image_analysis/"	
#gender_model = construct_model(2)
#gender_model.load(image_analysis_path + 'vgg_gender_model-80000')
#print("Complete - load gender model")

#category_model = construct_model(6)
#category_model.load(image_analysis_path + 'vgg_category_model-130000')
#print("Complete - load category model")
	

tl.init_graph(num_cores=8, gpu_memory_fraction=0.4)

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
vgg_network = dropout(network, 0.5)

image_analysis_path = "/home/dj/HighFashionProject/design_studio/image_analysis/"	

# Create your views here.
def classify_gender(request):
	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"
	X = generate_patches(img2numpy_arr(design_path + input_image_uid))

	num_classes = 2
	network_output = fully_connected(vgg_network, num_classes, activation='softmax')
	network_output = regression(network_output, optimizer='rmsprop',
						 loss='categorical_crossentropy',
						 learning_rate=0.00001)
	# Model
	gender_model = tl.DNN(network_output)
	gender_model.load(image_analysis_path + 'vgg_gender_model-80000')
	pred_y = gender_model.predict(X)
	return JsonResponse(
		{'results' : pred_y}
	)

def classify_category(request):
	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"
	X = generate_patches(img2numpy_arr(design_path + input_image_uid))

	num_classes = 6
	network_output = fully_connected(network, num_classes, activation='softmax')
	network_output = regression(network_output, optimizer='rmsprop',
						 loss='categorical_crossentropy',
						 learning_rate=0.00001)
	# Model
	category_model = tl.DNN(network_output)
	category_model.load(image_analysis_path + 'vgg_category_model-130000')
	pred_y = category_model.predict(X)
	return JsonResponse(
		{'results' : pred_y}
	)


