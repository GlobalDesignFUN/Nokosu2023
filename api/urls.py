from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('infos/', views.InfoList),
    path('infos/<str:pk>', views.InfoItem),
    path('users/register', views.registration),
    path('users/login', views.login),
    path('users/logout', views.logout),
    path('profiles/<str:pk>', views.profile),
    path('profiles/', views.profileList),
] 