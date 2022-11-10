from abc import ABC

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for MongoDB...")

