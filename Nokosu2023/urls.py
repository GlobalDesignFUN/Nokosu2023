from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import redirectbase, passwordReset

urlpatterns = [
    path('', redirectbase),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('password/<str:token>', passwordReset),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
