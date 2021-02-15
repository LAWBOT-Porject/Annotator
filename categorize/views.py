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
            print('############ ', categ_norme_id)
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
        temp.append( getattr(all_normes[i], 'date_debut'))
        temp.append( getattr(all_normes[i], 'date_fin'))
        normes.append(temp)
    return render(request, 'categorize.html', {"categories" : categories, "normes" : normes})
