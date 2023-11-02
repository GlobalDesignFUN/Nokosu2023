from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('infos/', views.infoList),
    path('infos/<str:pk>/', views.infoItem),
    path('groups/', views.groupList),
    path('groups/<str:pk>/', views.groupItem),
    path('users/register/', views.registration),
    path('users/login/', views.login),
    path('users/logout/', views.logout),
    path('profiles/<str:pk>/', views.profile),
    path('profiles/', views.profileList),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] 