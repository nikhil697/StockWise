import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run Flask app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Flask app...'))
        subprocess.Popen(['python', 'flask_app\app.py'])
