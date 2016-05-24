from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.MealCreateView.as_view(), name='meal-create'),
    url(r'^(?P<meal_id>[a-zA-Z0-9]+)/?$', views.MealServeView.as_view(), name='meal-serve'),
    url(r'^set_style/$', views.SetStyleView.as_view(), name='set-style'),

    url(r'^api/v1/$', views.MealCreateAPIView.as_view()),
)
