# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import time
from subprocess import Popen, PIPE, STDOUT

import numpy as np
import tensorflow as tf
import tflearn as tl
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.data import generate_patches, img2numpy_arr

def construct_simple_convnet(num_classes):
# Building 'Simple ConvNet'
	network = input_data(shape=[None, 42, 42, 3], name='input')

	network = conv_2d(network, 16, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = fully_connected(network, 256, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 256, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 2, activation='softmax')

	network = regression(network, optimizer='adam',
						 loss='categorical_crossentropy',
						 learning_rate=0.0001, name='target')

	model = tl.DNN(network)
	return model

image_analysis_path = "/home/dj/HighFashionProject/design_studio/image_analysis/"	

discriminator_model = construct_simple_convnet(2)
discriminator_model.load(image_analysis_path + 'discriminator_model-78000')

# Create your views here.
def classify_discriminator(image_path):
	X = generate_patches(img2numpy_arr(image_path))

	pred_y = discriminator_model.predict(X)
	return pred_y

def classify_fashion(request):
	X = generate_patches(img2numpy_arr(image_path))

	pred_y = analysis_model.predict(X)
	return pred_y
