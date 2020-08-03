from rest_framework import routers
from django.urls import path, include

from . import views


router = routers.DefaultRouter()
router.register('', views.UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('signin/', views.signin, name='signin'),
    path('signout/<int:id>/', views.signout, name='signout')
]