"""cloudstorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from cloudstorage.views import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/profile/$',
        api.ProfileView.as_view()),

    url(r'^api/login/$',
        api.LoginView.as_view()),

    url(r'^api/folders/$',
        api.FolderListAPIView.as_view()),

    url(r'^api/folders/(?P<folder_id>\d+)/$',
        api.FolderDetailAPIView.as_view()),

    url(r'^api/folders/(?P<folder_id>\d+)/files/$',
        api.FileListAPIView.as_view()),

    url(r'^api/folders/(?P<folder_id>\d+)/files/(?P<file_id>\d+)/$',
        api.FileDetailAPIView.as_view()),

    url(r'^api/folders/(?P<folder_id>\d+)/files/(?P<file_id>\d+)/file/$',
        api.FileRedirectAPIView.as_view()),



    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
