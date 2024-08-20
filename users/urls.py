from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
	path('login/', views.Login, name='Login'),
	path('signup/', views.signup, name='signup'),
	path('logout/', views.log_out, name='loggout'),
	path('', include('generator.urls')),
	


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)