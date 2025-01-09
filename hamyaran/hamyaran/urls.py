"""
URL configuration for hamyaran project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from services.views import home
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login, PasswordChange, Register, activate
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', include('services.urls')),
    path('', include('django.contrib.auth.urls')),
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$', activate, name='activate'),
    path("password_change/", PasswordChange.as_view(), name="password_change"),    
    path('', include('account.urls')),
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path('js-catalog', JavaScriptCatalog.as_view(), name='js-catalog'),
    path('webpush/', include('webpush.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)