import csv
from django.core.management.base import BaseCommand
from disgenet_app.models import Disease

class Command(BaseCommand):
    help = 'Importa doenças a partir de diseaseAttributes.csv'

    def handle(self, *args, **kwargs):
        with open('diseaseAttributes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                Disease.objects.update_or_create(
                    diseaseNID=row['diseaseNID'],
                    defaults={
                        'diseaseId': row['diseaseId'],
                        'diseaseName': row['diseaseName'],
                        'type': row['type'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
