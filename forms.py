from django.forms import Form, FileField, IntegerField, ChoiceField

from . models import Meal

class MealCreateForm(Form):
    file = FileField()
    expires_in = ChoiceField(choices=(
        (1, "1 minute"),
        (30, "30 minutes"),
        (60, "1 hour"),
        (180, "3 hours"),
        (60*24, "1 day"),
        (60*24*7, "1 week"),
    ), initial=30)
