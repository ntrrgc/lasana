from django.db.models import Model, CharField, FileField, DateTimeField
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage

from django.conf import settings

from django.utils import timezone

import string
import random

class MealStorage(FileSystemStorage):
    def url(self, name):
        return Meal.objects.get(file=name).get_absolute_url()

MEAL_ALPHABET = list(set(string.ascii_uppercase + string.digits) - {'I','1','O','0'})

safe_random = random.SystemRandom()

def get_random_string(length):
    return ''.join(safe_random.choice(MEAL_ALPHABET) for x in range(4))

class Meal(Model):
    id_length = 4
    id = CharField(max_length=id_length, db_index=True, primary_key=True)
    file = FileField(upload_to=settings.LASANA_UPLOAD_ROOT, verbose_name=_("File"), storage=MealStorage())
    expiration_time = DateTimeField(db_index=True, verbose_name=_("Expiration time"))

    def generate_auto_id(self):
        #Theoretically, we can have up to ~1 million meals, but having 10k would be enough to worry
        if Meal.objects.count() > 10000:
            raise RuntimeError("Too much meals")

        while True:
            random_string = get_random_string(length=4)
            if len(Meal.objects.filter(id=random_string)) == 0:
                self.id = random_string
                return self.id

    def is_expired(self, now=None):
        if not now:
            now = timezone.now()
        return now > self.expiration_time

    class Meta:
        ordering = ['expiration_time']
        verbose_name = _("Meal")

    def get_absolute_url(self):
        return reverse('meal-serve', kwargs={'meal_id': self.id})

    def __unicode__(self):
        now = timezone.now()
        if now > self.expiration_time:
            return "%s, expired for %s" % (self.file.url, now - self.expiration_time)
        else:
            return "%s, expires in %s" % (self.file.url, self.expiration_time - now)


def delete_file(sender, **kwargs):
    obj = kwargs['instance']
    if obj.file.name != "":
        obj.file.delete()

pre_delete.connect(delete_file, sender=Meal)
