from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, signUp, Logout, logIn

urlpatterns = [
    path('', home, name='home'),
    path('signUp', signUp, name='signUp'),
    path('logIn/', logIn, name='logIn'),
    path('logout/', Logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)