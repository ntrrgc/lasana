# -*- encoding: utf-8 -*- 
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Registers this node in the cluster'

    def set_site_info(self, site):
        # Assign a name (no distinction in this case) and save.
        site.name = u'La Saña'
        site.save() # Save to get an ID

        site.domain = settings.DOMAIN_FORMULA(site.id)
        site.save() # Update domain field

    @transaction.commit_on_success
    def handle(self, *args, **options):
        # Only one node should be registering at a time, acquire a lock
        cursor = connection.cursor()
        cursor.execute("lock registernode_mutex;");

        # Tries to read the node ID file
        try:
            with open('nodeid', 'r') as f:
                current_node_id = int(f.read())

            # Assert it is registered in the DB, and register it if not
            try:
                site = Site.objects.get(id=current_node_id)
                self.set_site_info(site)
            except ObjectDoesNotExist:
                site = Site(id=current_node_id)
                self.set_site_info(site)

        except IOError:
            # File does not exist, so we are not given a ID yet
            # Lets register!

            # Check if there is the example.com default domain (new installation).
            # If that's the case, modify it.
            # Modify it.
            if Site.objects.get(id=1).domain == 'example.com':
                site = Site.objects.get(id=1)
            else:
                # "Old" installation. Create a new site.
                site = Site()

            self.set_site_info(site)
            current_node_id = site.id

            # Write the new node id to file
            with open('nodeid', 'w') as f:
                f.seek(0)
                f.write(str(current_node_id))
                f.truncate()

        #Print this node domain
        self.stdout.write(site.domain)
