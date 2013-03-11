# -*- encoding: utf-8 -*- 
from django.core.management.base import BaseCommand, CommandError
from django.core.management import execute_from_command_line
from django.db import connection, transaction
import subprocess

class Command(BaseCommand):
    help = 'Acquires a lock in the database (table `syncdb_mutex`) and runs ' \
           'python manage.py syncdb then. Once ended, releases the lock.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        self.stdout.write('Acquiring syncdb_mutex lock...')
        cursor = connection.cursor()
        cursor.execute("lock syncdb_mutex;");
        self.stdout.write('Acquired!')

        subprocess.call(["python", "manage.py", "syncdb"] + list(args))

        self.stdout.write('Releasing syncdb_mutex lock...')
