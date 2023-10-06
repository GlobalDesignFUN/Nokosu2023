from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('infos/', views.InfoList),
    path('infos/<str:pk>', views.InfoItem),
] 