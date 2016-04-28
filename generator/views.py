import os
from subprocess import Popen, PIPE, STDOUT
import uuid
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def generator(request):
	image_generator_path = "/home/dj/HighFashionProject/image_generator/"
	os.chdir(image_generator_path)

	image_uid = str(uuid.uuid4())

	cmd = "gpu=0 batchSize=1 name="+image_uid+" net=checkpoints/experiment1_25_net_G.t7 th generate.lua" 
	gerenate_image = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : gerenate_image.stdout.read()}
	)
