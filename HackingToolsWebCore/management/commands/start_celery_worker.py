import time
from pathlib import Path
from django.core.management.base import BaseCommand
import os
import subprocess
import signal


class Command(BaseCommand):
    def ctrl_c_Function(self, signum, frame):
        time.sleep(1)
        self.stdout.write("Waiting for Celery...")

    def handle(self, *args, **options):
        signal.signal(signal.SIGINT, self.ctrl_c_Function)

        try:
            os.system(f"python -m celery -A HackingToolsWebCore worker -l info --concurrency=4 --without-gossip "
                      f"--pool=solo") 
        except Exception as ex:
            print(f'Error {ex} when try to start celery')
