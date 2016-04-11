from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

def design(request):
	return render(request, template_name='design.html')
