from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin
from django.shortcuts import render
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movie/', include('movie.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^$', views.index, name='index'),
    # error here 
    # url(r'.*', lambda request: render(request, '404.html'), name='404'),
    path('verification/', include('verify_email.urls')),] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)