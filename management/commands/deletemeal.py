from django.core.management.base import BaseCommand, CommandError

from lasana.models import Meal

class Command(BaseCommand):
    args = '<meal_id meal_id>'
    help = 'Deletes the meal with the specified id'

    def handle(self, *args, **options):
        for meal_id in args:
            try:
                meal = Meal.objects.get(id=int(meal_id))
            except Meal.DoesNotExist:
                raise CommandError('Meal "%s" does not exist' % meal_id)

            meal.delete()

            self.stdout.write('Successfully deleted meal "%s"\n' % meal_id)
