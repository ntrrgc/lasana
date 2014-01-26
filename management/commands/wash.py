from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError

from lasana.models import Meal

from django.utils import timezone

class Command(BaseCommand):
    args = ''
    help = 'Deletes expired meals'

    def handle(self, *args, **options):
        try:
            now = timezone.now()
            old_meals = Meal.objects.all().order_by("expiration_time")

            for meal in old_meals:
                if meal.is_expired(now):
                    meal_id = meal.id

                    meal.delete()
                    self.stdout.write('Thrown away expired meal "%s"\n' % meal_id)
                else:
                    break
        except:
            import traceback
            import sys
            print("----------------------------------------")
            print("Failed to wash meals.", file=sys.stderr)
            traceback.print_exc(sys.stderr)
            print("----------------------------------------")
