""" All the URLs, clearly """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_qrcodes', views.generate_qrcodes, name='generate_qrcodes'),
    path('all_runners', views.all_runners, name='all_runners'),
    path('view_qr_code', views.view_qr_code, name='view_qr_code'),
    path('view_athlete_details', views.view_athlete_details, \
        name='view_qrview_athlete_details_code'),
    path('register_for_run', views.register_for_run, name='register_for_run'),
    path('add_athlete_to_run', views.add_athlete_to_run, name='add_athlete_to_run'),
]
