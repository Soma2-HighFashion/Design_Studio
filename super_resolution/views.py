import os
from subprocess import Popen, PIPE, STDOUT
import uuid
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def super_resolution(request):
	super_resolution_path = "/home/dj/HighFashionProject/super_resolution/"
	os.chdir(super_resolution_path)

	generator_path = "/home/dj/HighFashionProject/HighFashionServer/static_files/generator/"
	input_image= str(request.GET['input'])
	output_uid = str(uuid.uuid4())

	cmd = "th waifu2x.lua -model_dir models/photo -m scale -i "+generator_path+input_image".png -o "+output_uid+".png" 
	gerenate_image = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : gerenate_image.stdout.read()}
	)
