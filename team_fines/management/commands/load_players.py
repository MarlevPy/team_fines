import json

from django.core.management.base import BaseCommand, CommandError
from fines.models import Player


class Command(BaseCommand):
    help = 'Load players from a json file into the Player model'

    def add_arguments(self, parser):
        parser.add_argument('-f', type=str)

    def handle(self, *args, **options):

        if len(Player.objects.all()) == 0:
            try:
                with open(options['f'], 'r') as f:
                    data = json.load(f)
            except TypeError:
                raise CommandError('Missing argument -f FILE_NAME')

            data = json.loads(data)

            for player in data:
                first_name = player.get('fields').get('first_name')
                last_name = player.get('fields').get('last_name')

                p = Player.objects.create(first_name=first_name, last_name=last_name)
                p.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(data)} players'))

        else:
            raise CommandError('The model Player is already populated, ensure that it is empty before running load_players.')
