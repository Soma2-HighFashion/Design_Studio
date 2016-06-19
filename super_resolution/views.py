import os
from subprocess import Popen, PIPE, STDOUT

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def super_resolution_x2(request):
	os.chdir(settings.SUPER_RESOLUTION_PATH)

	input_image_uid = str(request.GET['input'])
	cmd = (settings.TORCH_PATH + "th waifu2x.lua -model_dir models/photo -m scale " +
			" -i " + settings.GENERATOR_PATH + input_image_uid + 
			" -o " + settings.DESIGN_PATH + input_image_uid)

	gerenate_image = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : os.path.basename(gerenate_image.stdout.read()).strip() }
	)

def super_resolution_nr(request):
	os.chdir(settings.SUPER_RESOLUTION_PATH)

	input_image_uid = str(request.GET['input'])

	cmd = (settings.TORCH_PATH + "th waifu2x.lua -model_dir models/photo -m noise -noise_level 2" +
			" -i " + settings.GENERATOR_PATH + input_image_uid + 
			" -o " + settings.GENERATOR_PATH + input_image_uid )
	gerenate_image = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return JsonResponse(
		{'results' : os.path.basename(gerenate_image.stdout.read()).strip() }
	)
