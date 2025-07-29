from django.core.management.base import BaseCommand
from reminders.models import Reminder
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Initialize reminders for the application'

    def handle(self, *args, **kwargs):
        # Example initialization logic
        default_reminders = [
            {
            'title': 'Daily Check-in',
            'description': 'Remember to check your daily tasks.',
            'date': (datetime.utcnow() + timedelta(days=60)).isoformat() + 'Z',
            'is_done': False,
            },
            {
            'title': 'Weekly Review',
            'description': 'Review your week and plan for the next one.',
            'date': (datetime.utcnow() + timedelta(days=90)).isoformat() + 'Z',
            'is_done': False,
            },
        ]
        for reminder_data in default_reminders:
            Reminder.objects.get_or_create(**reminder_data)
        self.stdout.write(self.style.SUCCESS('Reminders initialized successfully.'))    