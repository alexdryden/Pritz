"""votingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView, TemplateView
from django.urls import path, include

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='about_urlpattern', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('webVotingApp.urls')),
    path('about/', TemplateView.as_view(template_name='webVotingApp/about.html'),
         name='about_urlpattern'),
    path('login/', LoginView.as_view(template_name='webVotingApp/login.html'),
         name='login_urlpattern'),
    path('logout/', LogoutView.as_view(), name='logout_urlpattern')

]
