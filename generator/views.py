import os
import time
from subprocess import Popen, PIPE, STDOUT
import uuid
from PIL import Image

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

from image_analysis.views import classify_discriminator, classify_fashion 

# Create your views here.
def generator(request):
	os.chdir(settings.DCGAN_PATH)
	image_uid = str(uuid.uuid4())

	# Generate Random Image

	cmd = ("gpu=0 noise=normal name="+image_uid+ " batchSize=" + str(settings.G_COUNT) +
			" net=checkpoints/fashionG_18_net_G.t7 th generate.lua")
	generate_image = Popen(cmd, shell=True, stdin=PIPE, 
							stdout=PIPE, stderr=STDOUT, close_fds=True)
	f_name = os.path.basename(generate_image.stdout.read()).strip()
	image_count = settings.G_COUNT

	pred_y = classify_discriminator(f_name)
	d_patch_count = settings.D_PATCH_COUNT

	#  Classify Generate Image - Good or Bad

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

	#  Find Best Image with Word2Vec  - Gender and Category

	pred_fashion = classify_fashion(f_name)
	f_patch_count = settings.F_PATCH_COUNT

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

		print "No.", (i+1), "Gender Result:\n", "Female-", female_count/f_patch_count,\
				"Male-", male_count/f_patch_count
		print "No.", (i+1), "Category Result:\n", "Street-", street_count, "Casual-",casual_count,\
				"\nClassic-",classic_count, "Unique-",unique_count, "Sexy-",sexy_count

	best_index = 5 #Temporary Value

	# Crop Best Image

	generator_path = settings.GENERATOR_PATH
	input_image = Image.open(generator_path + f_name)

	g_geometry = settings.G_GEOMETRY
	y,x = divmod(best_index, settings.G_IMAGE[1])
	left = x * g_geometry[1]
	right = (x+1) * g_geometry[1]
	top = y * g_geometry[0]
	bottom = (y+1) * g_geometry[0]

	best_image = input_image.crop((left, top, right, bottom)).save(generator_path+f_name)
	
	return JsonResponse(
		{'results' : f_name}
	)
