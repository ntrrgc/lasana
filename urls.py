from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.MealCreateView.as_view(), name='meal-create'),
    url(r'^(?P<meal_id>[A-Z0-9]+)/$', views.MealServeView.as_view(), name='meal-serve'),
)
