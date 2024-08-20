from django.conf import settings
from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
   

    path('', views.home, name='home'),
    path('imageG/', views.imageG, name='imageG'),
    path('miniG/', views.miniG, name='miniG'),
    path('minigoogle/', views.minigoogle, name='minigoogle'),
    path('image/', views.image_generator, name='image')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
