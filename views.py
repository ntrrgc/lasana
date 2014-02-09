from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import View, TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from . models import Meal
from . forms import MealCreateForm, MealCreateFormAPI
from . sendfile import send
from . import styles
from . settings import LASANA_ALLOW_CHANGE_STYLE, LASANA_BLOCK_CRAWLERS
import idn

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, \
        HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from django.core.urlresolvers import reverse, reverse_lazy

from datetime import timedelta
from django.utils import timezone
import json


def process_meal(request, file, expiration_time):
    meal = Meal(file=file, expiration_time=expiration_time)
    meal.generate_auto_id()
    meal.save()

    meal_serve_url = reverse('meal-serve', kwargs={'meal_id': meal.id})
    meal_serve_absolute_url = request.build_absolute_uri(meal_serve_url)
    #Transform URL to IDN Unicode
    meal_serve_absolute_url = idn.transform_url_to_idn(meal_serve_absolute_url)

    return meal, meal_serve_absolute_url


class MealCreateView(FormView):
    template_name = "lasana/meal_form.html"
    form_class = MealCreateForm

    def form_valid(self, form):
        expires_in = int(form.cleaned_data['expires_in'])
        file = form.cleaned_data['file']

        expiration_time = timezone.now() + timedelta(minutes=expires_in)

        meal, url = process_meal(self.request, file, expiration_time)

        return TemplateResponse(self.request, 
                                "lasana/meal_create_success.html",
                                context={'meal': meal,
                                         'meal_serve_absolute_url': url})


class MealCreateAPIView(FormView):
    template_name = "lasana/meal_form_api.html"
    form_class = MealCreateFormAPI
    
    def form_valid(self, form):
        expires_in = int(form.cleaned_data['expires_in'])
        file = form.cleaned_data['file']

        if form.cleaned_data['file_name_override'] != "":
            file.name = form.cleaned_data['file_name_override']

        expiration_time = timezone.now() + timedelta(minutes=expires_in)

        meal, url = process_meal(self.request, file, expiration_time)

        data = {
            'meal_id': meal.id,
            'url': url,
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def form_invalid(self, form):
        data = {
            'error': 'Invalid input',
            # Set to True if client must use a newer version of the API.
            'deprecated_version': False,
        }

        return HttpResponseBadRequest(json.dumps(data),
                                      content_type="application/json")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MealCreateAPIView, self).dispatch(*args, **kwargs)
    

class MealServeView(View):
    def forbidden_user_agent(self):
        user_agent = self.request.META['HTTP_USER_AGENT']
        return any(bot in user_agent
                   for bot in LASANA_BLOCK_CRAWLERS)

    def get(self, request, *args, **kwargs):
        if self.forbidden_user_agent():
            response = HttpResponseForbidden()
            response['X-Robots-Tag'] = 'noindex'
            return response

        #if there is no such meal, redirect to main page
        meal_iter = Meal.objects.filter(id=kwargs['meal_id'])
        if len(meal_iter) != 1:
            return self.no_meal()
        
        meal = meal_iter[0]

        #if meal is there, but has expired, throw it away and redirect to main page too
        if meal.is_expired():
            meal.delete()
            return self.no_meal()
        else:
            #else, serve the meal
            file = meal_iter[0].file
            return send(request, file)
    
    def no_meal(self):
        return HttpResponseRedirect(reverse('meal-create'))


class SetStyleView(View):
    def get(self, request, *args, **kwargs):
        if not LASANA_ALLOW_CHANGE_STYLE:
            raise PermissionDenied

        styles.set_style(request, request.GET.get('style'))

        redirect_to = request.META.get('HTTP_REFERER') or reverse('meal-create')
        return HttpResponseRedirect(redirect_to)
