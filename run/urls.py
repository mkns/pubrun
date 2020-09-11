""" All the URLs, clearly """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_qrcodes', views.generate_qrcodes, name='generate_qrcodes'),
    path('all_runners', views.all_runners, name='all_runners'),
    path('view_qr_code', views.view_qr_code, name='view_qr_code'),
]
