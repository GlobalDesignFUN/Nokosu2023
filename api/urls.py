from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('infos/', views.InfoList),
    path('infos/<str:pk>', views.InfoItem),
    path('user/register', views.registration),
    path('user/login', views.login),
    path('user/logout', views.logout),
] 