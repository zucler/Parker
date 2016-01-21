from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from parker.routers import CustomReadOnlyRouter
from parker.views import ParkingViewSet

from . import views


router = CustomReadOnlyRouter()
router.register(prefix='api', viewset=ParkingViewSet, base_name='model')


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    #url(r'^admin/', admin.site.urls),
    #url(r'^test_search/', views.test, name='Test search'),
    #url(r'^details/(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='vote'),
    #url(r'^search/', views.search_index, name='Parking search'),

    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')) # Remove in future

]
