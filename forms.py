from django.forms import Form, FileField, IntegerField, ChoiceField
from django.utils.translation import ugettext_lazy as _

from . models import Meal

class MealCreateForm(Form):
    file = FileField(label=_("File"))
    expires_in = ChoiceField(choices=(
        (1, _("1 minute")),
        (30, _("30 minutes")),
        (60, _("1 hour")),
        (180, _("3 hours")),
        (60*24, _("1 day")),
        (60*24*7, _("1 week")),
    ), initial=180, label=_("Expires in"))
