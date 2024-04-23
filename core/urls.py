"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from user_management.urls import urlpatterns as token_url_patterns
from portfolio_management.urls import asset_urls

v1_urlpatterns = [
    path(f'portfolio/', include((asset_urls,'orders')), name='portfolio')

]
urlpatterns = [
    path('api/v1/', include((v1_urlpatterns, 'v1')), name='v1 apis'),
    path('open_api/', include((token_url_patterns, 'token_v1'), namespace='token_v1')),
    path('admin/', admin.site.urls),
]
