import os
import time
from subprocess import Popen, PIPE, STDOUT
import uuid
from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.views import classify_discriminator, classify_fashion 

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
	print("Discriminator Result:", good_count/len(pred_y))

	pred_fashion = classify_fashion(f_name)
	female_count = 0; male_count = 0;
	street_count = 0; casual_count = 0; classic_count = 0; 
	unique_count = 0; sexy_count = 0;

	for f in pred_fashion:
		female_count += sum(f[0:5])
		male_count += sum(f[5:])
		street_count += (f[0] + f[5])
		casual_count += (f[1] + f[6])
		classic_count += (f[2] + f[7])
		unique_count += (f[3] + f[8])
		sexy_count += f[4]

	fashion_count = len(pred_fashion)
	print("Gender Result:", "Female-", female_count/fashion_count, "Male-", male_count/fashion_count)
	print("Category Result:", "Street-", street_count, "Casual-",casual_count, 
			"Classic-",classic_count, "Unique-",unique_count, "Sexy-",sexy_count)

	if good_count/len(pred_y) < 0.7:
		cmd2 = ("gpu=0 noise=normal name="+image_uid+
			" net=checkpoints/fashionG_18_net_G.t7 th generate.lua")
		generate_image2 = Popen(cmd2, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
		
	return JsonResponse(
		{'results' : image_uid + ".png"}
	)
