"""badeli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
	path('admin/', admin.site.urls),
	# ex: /polls/
	path('', views.HomePageView.as_view(), name='home'),
	path('signup/', views.badeli_signup, name='signup'),
	path('logout/', views.badeli_logout, name='logout'),
	path('login/', views.myLogin, name='login'),
	path('app/', TemplateView.as_view(template_name="app.html"), name='app'),
	path('search/', views.Search.as_view(), name='search'),
	# path('match/')
	# path('', views.index, name='index'),
]
