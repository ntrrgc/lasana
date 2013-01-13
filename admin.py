from django.contrib import admin
from . models import Meal

class MealAdmin(admin.ModelAdmin):
    pass

admin.site.register(Meal, MealAdmin)
