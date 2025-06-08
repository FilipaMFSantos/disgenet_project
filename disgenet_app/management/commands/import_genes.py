import csv
from django.core.management.base import BaseCommand
from disgenet_app.models import Gene

class Command(BaseCommand):
    help = 'Import genes from geneAttributes.csv'

    def handle(self, *args, **kwargs):
        with open('disgenet_app/geneAttributes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')  # usa tab como separador
            for row in reader:
                gene_name = row.get('geneName')
                if not gene_name:
                    self.stdout.write(self.style.WARNING(
                        f"Gene com geneId {row.get('geneId')} ignorado por não ter geneName."))
                    continue

                Gene.objects.create(
                    geneId=row.get('geneId'),
                    geneName=gene_name,
                    geneDescription=row.get('geneDescription', ''),
                    pLI=row.get('pLI') or None,
                    DSI=row.get('DSI') or None,
                    DPI=row.get('DPI') or None
                )
