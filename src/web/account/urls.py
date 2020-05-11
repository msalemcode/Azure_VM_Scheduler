from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.sign_in, name='sign_in'),
    path('signin/azure_ad', views.sign_in_azure_ad, name='sign_in_azure_ad'),
    path('signin/azure_ad/callback', views.sign_in_azure_ad_callback, name='sign_in_azure_ad_callback'),
    path('signout', views.sign_out, name='sign_out'),
    path('error', views.error, name='error'),
]