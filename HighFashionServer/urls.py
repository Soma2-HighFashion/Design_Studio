"""StorageServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from home.views import index, design
from generator.views import generator, ImageViewSet, DesignViewSet
from super_resolution.views import super_resolution_x2, super_resolution_nr
from image_analysis.views import classify_fashion, classify_discriminator, search_neighbors
	 
router = routers.DefaultRouter()
router.register(r'image', ImageViewSet)
router.register(r'design', DesignViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/', include(router.urls)),
	url(r'^$', index, name='index'),
	url(r'^design$', design, name='design'),
	url(r'^generator$', generator, name='generator'),
	url(r'^super_resolution_x2$', super_resolution_x2, name='super_resolution_x2'),
	url(r'^super_resolution_nr$', super_resolution_nr, name='super_resolution_nr'),
	url(r'^classify_discriminator$', classify_discriminator, name='classify_discriminator'),
	url(r'^classify_fashion$', classify_fashion, name='classify_fashion'),
	url(r'^search_neighbors$', search_neighbors, name='search_neighbors'),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT} ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static('uploaded', document_root=settings.MEDIA_ROOT)
