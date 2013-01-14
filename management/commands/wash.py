from django.core.management.base import BaseCommand, CommandError

from lasana.models import Meal

from django.utils import timezone

class Command(BaseCommand):
    args = ''
    help = 'Deletes expired meals'

    def handle(self, *args, **options):
        now = timezone.now()
        old_meals = Meal.objects.all().order_by("expiration_time")

        for meal in old_meals:
            if meal.is_expired(now):
                meal_id = meal.id

                meal.delete()
                self.stdout.write('Thrown away expired meal "%s"\n' % meal_id)
            else:
                break
