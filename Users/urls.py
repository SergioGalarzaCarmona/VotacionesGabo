from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, signUp, Logout, logIn, main, admin_votes, restart_votes

urlpatterns = [
    path('', home, name='home'),
    path('signUp', signUp, name='signUp'),
    path('logIn/', logIn, name='logIn'),
    path('logout/', Logout, name='logout'),
    path('main/', main, name='main'),
    path('admin_votes/', admin_votes, name='admin_votes'),
    path('restart_votes/', restart_votes, name='restart'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)