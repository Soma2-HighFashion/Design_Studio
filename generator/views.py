import os
import time
from subprocess import Popen, PIPE, STDOUT
import uuid
from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.views import classify_discriminator

# Create your views here.
def generator(request):
	image_generator_path = "/home/dj/HighFashionProject/word2image/dcgan"
#	image_generator_path = "/Users/Dongjun/HighFashionProject/word2image/dcgan"	
	os.chdir(image_generator_path)

	image_uid = str(uuid.uuid4())

	cmd = ("gpu=0 noise=normal name="+image_uid+
			" net=checkpoints/fashionG_18_net_G.t7 th generate.lua")
	generate_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	f_name = os.path.basename(generate_image.stdout.read()).strip()
		
	pred_y = classify_discriminator(f_name)
	good_count = 0; bad_count = 0

	for y in pred_y:
		good_count += y[1]
	
	print("Result:", good_count/len(pred_y))

	if good_count/len(pred_y) < 0.7:
		cmd2 = ("gpu=0 noise=normal name="+image_uid+
			" net=checkpoints/fashionG_18_net_G.t7 th generate.lua")
		generate_image2 = Popen(cmd2, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
		
	return JsonResponse(
		{'results' : image_uid + ".png"}
	)
