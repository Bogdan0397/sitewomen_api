"""drfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from drfsite import settings
from women.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/husbandslist/', HusbandAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/women/<slug:slug>/', WomenAPIRetrieve.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    path('api/v1/womencatlist/<slug:slug>/', WomenCategoryAPIView.as_view()),
    path('api/v1/womentaglist/<slug:slug>/', WomenTagAPIView.as_view()),
    path('api/v1/catlist/', CatAPIList.as_view()),
    path('api/v1/taglist/', TagAPIList.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/womenpublished/', WomenPublishedAPIList.as_view()),
    path('api/v1/users/', UserAPIListCreate.as_view(), name='user-list-create'),
    path('api/v1/user/<int:pk>/',UpdateRetrieveAPIUser.as_view(), name='profile-update'),
    path('api/v1/username/<str:email>/',UpdateStrRetrieveAPIUser.as_view(), name='profile-strupdate'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)