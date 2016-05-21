import os
from subprocess import Popen, PIPE, STDOUT
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def classify_gender(request):
	image_analysis_path = "/home/dj/HighFashionProject/image_analysis/"
	os.chdir(image_analysis_path)

	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"

	cmd = "python test_gender_vgg.py --test_file " + design_path+input_image_uid 
	pred_y_proba = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : pred_y_proba}
	)

def classify_category(request):
	image_analysis_path = "/home/dj/HighFashionProject/image_analysis/"
	os.chdir(image_analysis_path)

	input_image_uid = str(request.GET['input'])
	design_path = "/home/dj/HighFashionProject/design_studio/static_files/designed/"

	cmd = "python test_category_vgg.py --test_file " + design_path+input_image_uid 
	pred_y_proba = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : pred_y_proba}
	)
