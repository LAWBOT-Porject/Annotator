
from json import loads, dumps
from os.path import basename
from django.http import HttpResponse
from config.hparam import hparam as hp
from django.shortcuts import render, redirect
from annotate.models import (Juridiction as juridiction,
                            Ville as ville, 
                            Categorie,
                            Personne,
                            DecisionPersonne,
                            Demande,
                            Demander,
                            Defender,
                            Decision)

treated_files_folder = hp.files.treated_files_folder
default_dir = None

def annotate_view(request, directory=None, *args, **kwargs):
    if request.method == 'GET':
        files = []
        global default_dir
        if (directory != None):
            selected_dir = directory
            default_dir = directory
        elif (default_dir != None):
            selected_dir = default_dir
        else:
            selected_dir = treated_files_folder
            default_dir = selected_dir
        decisions = Decision.objects.filter(decision_treated_path__contains = selected_dir)
        for item in decisions:
            tmp = []
            decision_path = item.decision_treated_path
            tmp.append(basename(decision_path))
            tmp.append(decision_path)
            files.append(tmp)
        return render(request, 'annotate.html', 
        {"files": files, 'file_list_len': len(files),})
    if request.method == 'POST':
        if 'read' in request.path:
            return read_file(request) 
        if 'get_default_category' in request.path:
            return get_category_by_nppac(request)
        # if 'submit_individual_demande' in request.path:
        #     return submit_demand(request, request.path[-1])
        data = request.POST
        current_decision = ''
        current_decision_id = ''
        try:
            ##TODO : specify the user id to get the decision annotated by the current user
            current_decision = Decision.objects.filter(decision_treated_path__contains= data['file-name'])[0] #.get(annotator_id=current_user)
            current_decision_id = getattr(current_decision, 'id')
        except Decision.DoesNotExist:
            print('Decision exception')
        decision_text = getattr(current_decision, 'texte_decision')
        
        for i in range(int(data['juges-number'])):
            titre_j = data['juge-'+str(i+1)+'-titre']
            nom_j = data['juge-'+str(i+1)+'-nom']
            prenom_j = data['juge-'+str(i+1)+'-prenom']
            
            if nom_j and nom_j != '':
                nom_position_j = decision_text.find(nom_j)
            else:
                nom_position_j = -1

            if prenom_j and prenom_j != '':
                prenom_position_j = decision_text.find(prenom_j)
            else:
                prenom_position_j = -1

            if titre_j and titre_j != '':
                if nom_position_j != -1:
                    titre_position_j = decision_text[nom_position_j-50:nom_position_j].find(titre_j)
                elif prenom_position_j != -1:
                    titre_position_j = decision_text[prenom_position_j-50:prenom_position_j].find(titre_j)
                else:
                    titre_position_j = decision_text.find(titre_j)
            else:
                titre_position_j = -1

            new_juge = Personne.objects.create(titre= titre_j,
                                                nom= nom_j,
                                                prenom= prenom_j,
                                                titre_position= titre_position_j,
                                                nom_position= nom_position_j,
                                                prenom_position= prenom_position_j
                                            )
            DecisionPersonne.objects.create(decision_id= current_decision,
                                            person_id = new_juge,
                                            fonction = 'juge-'+str(i+1))
        
        for i in range(int(data['parties-number'])):
            
            try:
                titre_j = data['partie-'+str(i+1)+'-titre']
                nom_j = data['partie-'+str(i+1)+'-nom']
                prenom_j = data['partie-'+str(i+1)+'-prenom']
                dob_j = data['partie-'+str(i+1)+'-dob']
                adr_j = data['partie-'+str(i+1)+'-adr']
            except Exception as e:
                print(e)
            
            try:    
                nom_entreprise_j = data['partie-'+str(i+1)+'-nom-entreprise']
                siret_j = data['partie-'+str(i+1)+'-siret']
                naf_j = data['partie-'+str(i+1)+'-naf']
                adr_entreprise_j = data['partie-'+str(i+1)+'-adr-entreprise']
            except Exception as e:
                print(e)
            
            if nom_entreprise_j != '' or siret_j != '' or naf_j != '' or adr_entreprise_j != '':
                
                if nom_entreprise_j and nom_entreprise_j != '':
                    nom_entreprise_position_j = decision_text.find(nom_entreprise_j)
                else:
                    nom_entreprise_position_j = -1
                
                if siret_j and siret_j != '':
                    siret_position_j = decision_text.find(siret_j)
                else:
                    siret_position_j = -1
                
                if naf_j and naf_j != '':
                    naf_position_j = decision_text.find(naf_j)
                else:
                    naf_position_j = -1

                if adr_entreprise_j and adr_entreprise_j != '':
                    adr_entreprise_position_j = decision_text.find(adr_entreprise_j)
                else:
                    adr_entreprise_position_j = -1
                
                new_personne_morale = Personne.objects.create(  nom = nom_entreprise_j,
                                                                adresse= adr_entreprise_j,
                                                                siret = siret_j,
                                                                naf = naf_j,
                                                                physique= False,
                                                                nom_position = nom_position_j,
                                                                adresse_position = adr_entreprise_position_j,
                                                                naf_position = naf_position_j,
                                                                siret_position = siret_position_j
                                                            )
                
                DecisionPersonne.objects.create(person_id = new_personne_morale, 
                                                decision_id= current_decision,
                                                fonction= 'partie-'+str(i+1))

            else :
                
                if nom_j and nom_j != '':
                    nom_position_j = decision_text.find(nom_j)
                else:
                    nom_position_j = -1

                if prenom_j and prenom_j != '':
                    prenom_position_j = decision_text.find(prenom_j)
                else:
                    prenom_position_j = -1

                if titre_j and titre_j != '':
                    if nom_position_j != -1:
                        titre_position_j = decision_text[nom_position_j-50:nom_position_j].find(titre_j)
                    elif prenom_position_j != -1:
                        titre_position_j = decision_text[prenom_position_j-50:prenom_position_j].find(titre_j)
                    else:
                        titre_position_j = decision_text.find(titre_j)
                else:
                    titre_position_j = -1

                if dob_j and dob_j != '':
                    dob_position_j = decision_text.find(dob_j)
                else:
                    dob_position_j = -1
                
                if adr_j and adr_j != '':
                    adr_position_j = decision_text.find(adr_j)
                else:
                    adr_position_j = -1
                
                new_personne_physique = Personne.objects.create(  
                                                                  titre = titre_j,
                                                                  nom = nom_j,
                                                                  prenom = prenom_j,
                                                                  birth_date = dob_j,
                                                                  adresse= adr_j,
                                                                  titre_position = titre_position_j,
                                                                  nom_position = nom_position_j,
                                                                  prenom_position = prenom_position_j,
                                                                  birth_date_position = dob_position_j,
                                                                  adresse_position = adr_position_j
                                                            )
                
                DecisionPersonne.objects.create(person_id = new_personne_physique, 
                                                decision_id= current_decision,
                                                fonction= 'partie-'+str(i+1))
        
        if default_dir != treated_files_folder:
            print('with folder')
            return redirect('/annotate/'+ default_dir )
        else:
            print('without folder')
            return redirect('/annotate/' )

## Not used
def submit_demand(request, tab_idx):
    if request.method == 'POST':
        data = request.POST
        return HttpResponse(dumps({"demande_submission":"yes"}), content_type='application/json')
    return HttpResponse(dumps({"demande_submission":"no"}), content_type='application/json')

from json import loads
def read_file(request ):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    file = body['path']
    file_name = body['file_name']
    f = open(file, 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
    file_name = file_name.split('.')[0].split('-')
    try:
        city = ville.objects.filter(zip_code=file_name[1])[0].ville
    except:
        city = ''
    try:
        juridic = juridiction.objects.filter(abbreviation= file_name[0], zip_code__isnull=True)[0].type_juridiction
    except:
        juridic = ''
    rg = file_name[2]
    context = {
        'city': city,
        'juridiction': juridic,
        'rg': rg,
        'file': file_content
    }
    data = dumps(context)
    return HttpResponse(data, content_type='application/json')

def get_category_by_nppac (request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    nppac = body['nppac']
    try:
        default_categorie = Categorie.objects.get(noppac = nppac)
        default_categorie = getattr(default_categorie, 'description')
    except Categorie.DoesNotExist :
        default_categorie = '##### Catégorie non trouvée #####'
        nppac = ''
    data = dumps({"nppac": nppac, "default_categorie": default_categorie})
    return HttpResponse(data, content_type='application/json')
