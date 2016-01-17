from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^test_search/', views.test, name='Test search'),
    url(r'^details/(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='vote')
    url(r'^search/', views.search, name='Parking search')
]
