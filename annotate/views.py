
from json import loads, dumps
from os.path import basename
from django.http import HttpResponse
from config.hparam import hparam as hp
from django.shortcuts import render, redirect
from fuzzywuzzy import fuzz
from helpers.upload_utilities import transform_to_standard_chars as string_transform
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
        """ print('######################')
        for k in data:
            if(k != 'file-content'):
                print(f'{k}: #{data[k]}#')
        print('######################') """
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
        
        parties = []
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
                parties.append(new_personne_morale)
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
                parties.append(new_personne_physique)
                DecisionPersonne.objects.create(person_id = new_personne_physique, 
                                                decision_id= current_decision,
                                                fonction= 'partie-'+str(i+1))
        
        for i in range(int(data['avocats-number'])):
            titre_j = data['avocat-'+str(i+1)+'-titre']
            nom_j = data['avocat-'+str(i+1)+'-nom']
            prenom_j = data['avocat-'+str(i+1)+'-prenom']
            bareau_j = data['avocat-'+str(i+1)+'-bareau']

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

            if bareau_j and bareau_j != '':
                bareau_position_j = decision_text.find(bareau_j)
            else:
                bareau_position_j = -1

            new_avocat = Personne.objects.create(titre= titre_j,
                                                nom= nom_j,
                                                prenom= prenom_j,
                                                titre_position= titre_position_j,
                                                nom_position= nom_position_j,
                                                prenom_position= prenom_position_j
                                            )
            avocat_person = DecisionPersonne.objects.create(decision_id= current_decision,
                                            person_id = new_avocat,
                                            fonction = 'avocat-'+str(i+1),
                                            barreau=bareau_j,
                                            barreau_position= bareau_position_j )
            for j in range(len(parties)):
                try:
                    if(data['avocat-'+str(i+1)+'-partie-'+str(j+1)]):
                        avocat_person.person2_id.add(parties[j])
                except Exception as e:
                    print(e)

        if(data['decision-rg'] != ''):
            current_decision.rg = data['decision-rg']
            current_decision.rg_position = decision_text.find(data['decision-rg'])

        if(data['decision-chambre'] != ''):
            current_decision.chambre = data['decision-chambre']
            current_decision.chambre_position = decision_text.find(data['decision-chambre'])

        if(data['decision-date'] != ''):
            current_decision.date = data['decision-date']
            current_decision.date_position = decision_text.find(data['decision-date'])

        # Corbeille
        try:
            if(data['corbeille']):
                current_decision.corbeille = True
        except Exception as e:
            print(e)
        
        if(data['decision-ville'] != ''):
            current_decision.zip_code_position = decision_text.find(data['decision-ville'])
            try:
                current_decision_ville = ville.objects.get(ville = data['decision-ville'])
            except ville.DoesNotExist as e :
                try:
                    current_decision_ville = ville.objects.get(ville = data['decision-ville'].capitalize())
                except ville.DoesNotExist:
                    city_in_text = string_transform(data['decision-ville']).lower()
                    all_villes = ville.objects.all()
                    cities     = [city.ville for city in all_villes]
                    biggest_ration = 0
                    potential_city = ''
                    for city in cities :
                        cmp_city = string_transform(city).lower()
                        temp_ratio = fuzz.ratio(cmp_city, city_in_text)
                        position = city_in_text.find(cmp_city)
                        if (temp_ratio >=95 or (position != -1)):
                            try:
                                current_decision_ville = ville.objects.get(ville = city)
                                print(current_decision_ville)
                                break
                            except ville.DoesNotExist as e:
                                print(e)
                                new_ville = ville.objects.create(zip_code='9999', ville= data['decision-ville'].capitalize())

        if(data['decision-juridiction'] != ''):
            current_decision.juridiction_position = decision_text.find(data['decision-juridiction'])
            if current_decision_ville:
                try:
                    current_decision.juridiction_id = juridiction.objects.filter(zip_code=current_decision_ville).get(type_juridiction= data['decision-juridiction'].capitalize())
                except juridiction.DoesNotExist as e:
                    print(e)
                    current_decision.juridiction_id = juridiction.objects.create(zip_code=current_decision_ville, type_juridiction= data['decision-juridiction'].capitalize())
            else:
                if new_ville :
                    current_decision.juridiction_id = juridiction.objects.create(zip_code=new_ville, type_juridiction= data['decision-juridiction'].capitalize())

        current_decision.annotation_state = 2
        current_decision.annotator_id = request.user

        for i in range(int(data['demandes-number'])):
            try:
                if(data['hidden-nppac-demand-'+str(i+1)] != ''):
                    try:
                        current_categorie = Categorie.objects.get(noppac = data['hidden-nppac-demand-'+str(i+1)])
                        new_demand = Demande.objects.create(categorie_id=current_categorie, decision_id= current_decision)
                    except Categorie.DoesNotExist as e :
                        print(e)
                        new_demand = Demande.objects.create( decision_id= current_decision)
                else :

                    new_demand = Demande.objects.create( decision_id= current_decision)
            except Exception as e:
                print(e)
                new_demand = Demande.objects.create( decision_id= current_decision)

            if (data['montant-demande-'+str(i+1)] != ''):
                new_demand.montant_demande = data['montant-demande-'+str(i+1)]
                new_demand.montant_demande_position = decision_text.find(data['montant-demande-'+str(i+1)])

            if (data['unite-demande-'+str(i+1)] != ''):
                new_demand.unite_demande = data['unite-demande-'+str(i+1)]
                new_demand.unite_demande_position = decision_text.find(data['unite-demande-'+str(i+1)])

            if (data['quantite-demande-'+str(i+1)] != ''):
                new_demand.quantite_demande = data['quantite-demande-'+str(i+1)]
                new_demand.quantite_demande_position = decision_text.find(data['quantite-demande-'+str(i+1)])

            if (data['montant-resultat-'+str(i+1)] != ''):
                new_demand.montant_resultat = data['montant-resultat-'+str(i+1)]
                new_demand.montant_resultat_position = decision_text.find(data['montant-resultat-'+str(i+1)])

            if (data['unite-resultat-'+str(i+1)] != ''):
                new_demand.unite_resultat = data['unite-resultat-'+str(i+1)]
                new_demand.unite_resultat_position = decision_text.find(data['unite-resultat-'+str(i+1)])

            if (data['quantite-resultat-'+str(i+1)] != ''):
                new_demand.quantite_resultat = data['quantite-resultat-'+str(i+1)]
                new_demand.quantite_resultat_position = decision_text.find(data['quantite-resultat-'+str(i+1)])

            if (data['pretention-'+str(i+1)] != ''):
                new_demand.pretention = data['pretention-'+str(i+1)]
                new_demand.pretention_position = decision_text.find(data['pretention-'+str(i+1)])

            if (data['motifs-'+str(i+1)] != ''):
                new_demand.dispositifs = data['motifs-'+str(i+1)]
                new_demand.dispositifs_position = decision_text.find(data['motifs-'+str(i+1)])

            if (data['dispositifs-'+str(i+1)] != ''):
                new_demand.motifs = data['dispositifs-'+str(i+1)]
                new_demand.motifs_position = decision_text.find(data['dispositifs-'+str(i+1)])

            try:
                if(data['accept-'+str(i+1)]):
                    new_demand.resultat = True
            except Exception as e:
                print(e)

            try:
                if(data['mauvaise-'+str(i+1)]):
                    new_demand.mauvaise_categorie = True
            except Exception as e:
                print(e)

            new_demand.save()

            
            for j in range(len(parties)):
                try:
                    ##TODO : Verify if a party can both demander and defender
                    # 'demande-1-partiedemandeur-1'
                    # 'demande-1-partiedefendeur-1'
                    if(data['demande-'+str(i+1)+'-partiedemandeur-'+str(j+1)]):
                        # Demander.objects.create()
                        Demander.objects.create(demande_id=new_demand, person_id=parties[j])
                        print(data['demande-'+str(i+1)+'-partiedemandeur-'+str(j+1)])
                    elif (data['demande-'+str(i+1)+'-partiedefendeur-'+str(j+1)]):
                        Defender.objects.create(demande_id=new_demand, person_id=parties[j])
                        print(data['demande-'+str(i+1)+'-partiedefendeur-'+str(j+1)])
                    else:
                        continue

                except Exception as e:
                    print(e)

        current_decision.save()
        
        if default_dir != treated_files_folder:
            return redirect('/annotate/'+ default_dir )
        else:
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
    # file = body['path']
    file_name = body['file_name']
    print(file_name)
    """ f = open(file, 'r', encoding='utf-8')
    file_content = f.read()
    f.close() """
    file_name_splited = file_name.split('.')[0].split('-')
    rg = file_name_splited[2]
    uuid = file_name_splited[3]
    try:
        current_decision = Decision.objects.filter(decision_treated_path__contains=body['file_name']).filter(annotation_state=0)[0]
        if (getattr(current_decision, 'annotation_state') == 2):
            file_content = 'Décision déjà annotée! Merci de choisir une autre'
            red = True
        else :
            file_content = current_decision.texte_decision
            red = False
    except Decision.DoesNotExist as e:
        print(e)
        red = False
        file_content = 'Décision n ' 'est pas trouvée!'
    
    try:
        city = ville.objects.filter(zip_code=file_name_splited[1])[0].ville
    except:
        city = ''
    try:
        juridic = juridiction.objects.filter(abbreviation= file_name_splited[0], zip_code__isnull=True)[0].type_juridiction
    except:
        juridic = ''
    
    context = {
        'city': city,
        'juridiction': juridic,
        'rg': rg,
        'file': file_content,
        'red': red
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
