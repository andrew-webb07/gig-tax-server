"""gig_tax_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from gigtaxapi.models.musician import Musician
from gigtaxapi.views import register_user, login_user, GigView, ReceiptView, TourView, MusicianView

# route the URL to the proper viewset and add a new URL mapping to the default router
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gigs', GigView, 'gig')
router.register(r'receipts', ReceiptView, 'receipt')
router.register(r'tours', TourView, 'tour')
router.register(r'musicians', MusicianView, 'musician')

urlpatterns = [
    path('register', register_user),
    path('', include(router.urls)),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
