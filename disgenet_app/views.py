import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
from .models import Gene, Disease, DiseaseClass, Disease2Class, VariantDisease
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def gene_list(request):
    query = request.GET.get("q", "")
    pli_filter = request.GET.get("pli_filter", "")

    genes = Gene.objects.all()

    if query:
        genes = genes.filter(geneName__icontains=query)

    if pli_filter == ">0.9":
        genes = genes.filter(pLI__gt=0.9)
    elif pli_filter == ">0.5":
        genes = genes.filter(pLI__gt=0.5)
    elif pli_filter == "0":
        genes = genes.filter(pLI__isnull=True)

    return render(request, "gene_list.html", {
        "genes": genes,
        "current_query": query,
        "current_pli": pli_filter
    })


def disease_info(request):
    diseases = []
    query = ""
    class_map = {}

    if request.method == "POST":
        query = request.POST.get("diseaseName", "").strip()
        if query:
            diseases = Disease.objects.filter(diseaseName__icontains=query)

            # Mapeamento das classes
            d2c = Disease2Class.objects.filter(diseaseNID__in=[d.diseaseNID for d in diseases])
            d2c_map = {item.diseaseNID: item.diseaseClassNID for item in d2c}

            disease_classes = DiseaseClass.objects.filter(
                diseaseClassNID__in=d2c_map.values()
            )

            class_map = {item.diseaseClassNID: item.diseaseClassName for item in disease_classes}

    return render(request, "disease_info.html", {
        "diseases": diseases,
        "query": query,
        "class_map": class_map
    })


def evolution_chart(request):
    try:
        vd = pd.DataFrame.from_records(VariantDisease.objects.all().values('diseaseNID', 'year'))
        dis = pd.DataFrame.from_records(Disease.objects.all().values('diseaseNID', 'type'))
        d2c = pd.DataFrame.from_records(Disease2Class.objects.all().values())
        dc = pd.DataFrame.from_records(DiseaseClass.objects.all().values())

        merged = vd.merge(dis, on='diseaseNID', how='left')
        merged = merged.merge(d2c, on='diseaseNID', how='left')
        merged = merged.merge(dc, on='diseaseClassNID', how='left')

        evolution = merged.groupby(['year', 'diseaseClassName']).size().reset_index(name='count')

        fig, ax = plt.subplots(figsize=(12, 6))
        for cls in evolution['diseaseClassName'].dropna().unique():
            data = evolution[evolution['diseaseClassName'] == cls]
            ax.plot(data['year'], data['count'], label=cls)
        ax.legend()
        ax.set_title('Evolução temporal por classe de doença')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Nº de registos')

        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        graphic = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        return render(request, 'evolution_chart.html', {'graphic': graphic})

    except Exception as e:
        return render(request, 'evolution_chart.html', {'error': str(e)})


def about_page(request):
    graphic = None
    try:
        vd = pd.DataFrame.from_records(VariantDisease.objects.all().values('diseaseNID', 'year'))
        dis = pd.DataFrame.from_records(Disease.objects.all().values('diseaseNID', 'type'))
        d2c = pd.DataFrame.from_records(Disease2Class.objects.all().values())
        dc = pd.DataFrame.from_records(DiseaseClass.objects.all().values())

        merged = vd.merge(dis, on='diseaseNID', how='left')
        merged = merged.merge(d2c, on='diseaseNID', how='left')
        merged = merged.merge(dc, on='diseaseClassNID', how='left')

        evolution = merged.groupby(['year', 'diseaseClassName']).size().reset_index(name='count')

        fig, ax = plt.subplots(figsize=(10, 5))
        for cls in evolution['diseaseClassName'].dropna().unique():
            data = evolution[evolution['diseaseClassName'] == cls]
            ax.plot(data['year'], data['count'], label=cls)
        ax.legend()
        ax.set_title('Evolução temporal por classe de doença')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Nº de registos')

        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        graphic = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

    except Exception as e:
        graphic = None

    return render(request, "about.html", {"graphic": graphic})

