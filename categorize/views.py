from django.shortcuts import render
from annotate.models import Categorie, Norme, CategorieNorme

def categorize_view(request):
    all_categories = Categorie.objects.all()
    categories = []
    for i in range( len(all_categories)):
        temp = []
        temp.append(i+1)
        temp.append( getattr(all_categories[i], 'noppac'))
        temp.append(getattr(all_categories[i], 'description'))
        temp.append(getattr(all_categories[i], 'objet'))
        # all_categ_norme = CategorieNorme.objects.filter(categorie_id__noppac == getattr(all_categories[i], 'noppac'))
        all_categ_norme = CategorieNorme.objects.filter(categorie_id = getattr(all_categories[i], 'noppac'))
        normes_fondements = []
        for categ_norme in all_categ_norme:
            categ_norme_id = getattr(categ_norme, 'norme_id_id')
            normes_fondements.append(getattr(Norme.objects.get(id=int(categ_norme_id)),'fondement' ))
        temp.append(normes_fondements)
        categories.append(temp)
    
    all_normes = Norme.objects.all()
    normes = []
    for i in range(len(all_normes)):
        temp = []
        temp.append(i+1)
        temp.append( getattr(all_normes[i], 'fondement'))
        temp.append( getattr(all_normes[i], 'texte_norme'))
        date = getattr(all_normes[i], 'date_debut')
        temp.append( "" if not date else date)
        date = getattr(all_normes[i], 'date_fin')
        temp.append( "" if not date else date)
        temp.append( getattr(all_normes[i], 'id'))
        normes.append(temp)
    return render(request, 'categorize.html', {"categories" : categories, "normes" : normes})

def create_norme(request):
    if request.method == 'POST':
        new_fondement = request.POST.get('new-fondement')
        new_descriptif = request.POST.get('new-descriptif')
        new_date_debut = request.POST.get('new-date-debut')
        if not new_date_debut: new_date_debut = None
        new_date_fin = request.POST.get('new-date-fin')
        if not new_date_fin: new_date_fin = None
        new_norme = Norme.objects.create(fondement= new_fondement,
                             texte_norme=new_descriptif,
                             date_debut=new_date_debut,
                             date_fin=new_date_fin)
        related_categories = request.POST.getlist('related-categ')
        print(related_categories)
        for item in related_categories:
            item = Categorie.objects.get(noppac=item)
            CategorieNorme.objects.create(categorie_id=item, norme_id=new_norme)
    return categorize_view(request)

def create_category(request):
    if request.method == 'POST':
        new_categorie = Categorie.objects.create(noppac= request.POST.get('new-noppac'),
                                                description=request.POST.get('new-description'),
                                                objet=request.POST.get('new-objet'))
        for id_ in request.POST.getlist('related-norme'):
            CategorieNorme.objects.create(categorie_id=new_categorie, norme_id=Norme.objects.get(id=id_))
    return categorize_view(request)
