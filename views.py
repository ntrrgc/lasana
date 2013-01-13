from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import View, TemplateResponse

from . models import Meal
from . forms import MealCreateForm
from . sendfile import send

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse, reverse_lazy

from datetime import timedelta
from django.utils import timezone

class MealCreateView(FormView):
    template_name = "lasana/meal_form.html"
    form_class = MealCreateForm
    
    def form_valid(self, form):
        expires_in = int(form.cleaned_data['expires_in'])
        file = form.cleaned_data['file']

        expiration_time = timezone.now() + timedelta(minutes=expires_in)

        meal = Meal(file=file, expiration_time=expiration_time)
        meal.generate_auto_id()
        meal.save()

        meal_serve_url = reverse('meal-serve', kwargs={'meal_id': meal.id})
        meal_serve_absolute_url = self.request.build_absolute_uri(meal_serve_url)

        return TemplateResponse(self.request, 
                                "lasana/meal_create_success.html",
                                context={'meal': meal,
                                         'meal_serve_absolute_url': meal_serve_absolute_url})
    

class MealServeView(View):
    def get(self, request, *args, **kwargs):
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
