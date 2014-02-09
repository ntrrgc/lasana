from django.forms import Form, FileField, IntegerField, CharField, ChoiceField
from django.utils.translation import ugettext_lazy as _

from . models import Meal

class MealCreateForm(Form):
    file = FileField(label=_("File"))
    expires_in = ChoiceField(choices=(
        (1, _("1 minute")),
        (30, _("30 minutes")),
        (60, _("1 hour")),
        (180, _("3 hours")),
        (360, _("6 hours")),
        (60*24, _("1 day")),
        (60*24*7, _("1 week")),
    ), initial=360, label=_("Expires in"))


class MealCreateFormAPI(MealCreateForm):
    file_name_override = CharField(max_length=100, required=False)
