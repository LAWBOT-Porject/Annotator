from django.contrib import admin
from .models import (Ville, Juridiction, Decision, 
                    Personne, DecisionPersonne,
                    Categorie, Demande, Demander, Defender, Norme, CategorieNorme)

admin.site.register(Ville)
admin.site.register(Juridiction)
admin.site.register(Decision)
admin.site.register(Personne)
admin.site.register(DecisionPersonne)
admin.site.register(Categorie)
admin.site.register(Demande)
admin.site.register(Demander)
admin.site.register(Defender)
admin.site.register(Norme)
admin.site.register(CategorieNorme)
