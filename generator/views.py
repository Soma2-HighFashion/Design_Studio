import os
import subprocess
import uuid
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def generator(request):
	os.chdir("./../image-generator-master")
	image_uid = str(uuid.uuid4())
	generate_image = subprocess.check_output("gpu=0 batchSize=1 name="+image_uid+" net=checkpoints/celebA_25_net_G.t7 th generate.lua", shell=True)

	return JsonResponse(
			{'results' : str(generate_image).strip()}
	)
