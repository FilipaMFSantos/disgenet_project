from django.db import models

class Gene(models.Model):
    geneNID = models.IntegerField(primary_key=True)
    geneId = models.CharField(max_length=20)
    geneName = models.CharField(max_length=255)
    geneDescription = models.TextField(null=True)
    pLI = models.FloatField(null=True)
    DSI = models.FloatField(null=True)
    DPI = models.FloatField(null=True)

    class Meta:
        db_table = 'geneAttributes'

class Disease(models.Model):
    diseaseNID = models.IntegerField(primary_key=True)
    diseaseId = models.CharField(max_length=20)
    diseaseName = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    class Meta:
        db_table = 'diseaseAttributes'

class DiseaseClass(models.Model):
    diseaseClassNID = models.IntegerField(primary_key=True)
    vocabulary = models.CharField(max_length=50)
    diseaseClass = models.CharField(max_length=10)
    diseaseClassName = models.CharField(max_length=255)

    class Meta:
        db_table = 'diseaseClass'

class Disease2Class(models.Model):
    diseaseNID = models.IntegerField()
    diseaseClassNID = models.IntegerField()

    class Meta:
        db_table = 'disease2class'

class VariantDisease(models.Model):
    NID = models.IntegerField(primary_key=True)
    diseaseNID = models.IntegerField()
    variantNID = models.IntegerField()
    source = models.CharField(max_length=50)
    year = models.IntegerField(null=True)

    class Meta:
        db_table = 'variantDiseaseNetwork'
