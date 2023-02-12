import time
from pathlib import Path
from django.core.management.base import BaseCommand
import os
import subprocess
import signal


class Command(BaseCommand):
    def ctrl_c_Function(self, signum, frame):
        time.sleep(1)
        os.system('docker start rabbitmq')
        os.system('docker start mongodb5')

    def handle(self, *args, **options):
        signal.signal(signal.SIGINT, self.ctrl_c_Function)

        try:
            os.system(f"docker build -t custom-rabbitmq:3.8-management-alpine"
                      f" HackingToolsWebCore\\management\\commands\\DockerSetUpFiles")
            self.stdout.write("Docker Built!")

            os.system('docker compose -p hacking_tools_web -f'
                      'HackingToolsWebCore\\management\\commands\\DockerSetUpFiles\\docker-compose.yml up')
            self.stdout.write("Docker Composed!")
        except Exception as ex:
            print(f'Error {ex} when try to create dockers')
