from django.db import models
from django.conf import settings

class Ville(models.Model):
    """ class Meta:
        unique_together = (('zip_code', 'ville'),) """
    zip_code = models.CharField(max_length=10)#, primary_key=True)
    ville = models.TextField(default='', null=True)
    
    def __str__(self):
        return ' '.join([self.ville, self.zip_code, self.pays])

class Juridiction(models.Model):
    type_juridiction = models.TextField(default='', null=True)
    abbreviation = models.TextField(default='', null=True)
    zip_code = models.ForeignKey(Ville,
                                on_delete=models.SET_NULL, null=True,)
    
    def __str__(self):
        return ' '.join([self.type_juridiction,
                        self.zip_code ])

## TO DO : Add juridiction foreignKey
class Decision(models.Model):
    rg = models.CharField(max_length=20, default='',)
    chambre = models.CharField(max_length=50, default='', )
    date = models.CharField(max_length=100,default='',)
    # Position fields
    rg_position          = models.IntegerField(default=-1)
    chambre_position     = models.IntegerField(default=-1)
    juridiction_position = models.IntegerField(default=-1)
    zip_code_position    = models.IntegerField(default=-1)
    date_position    = models.IntegerField(default=-1)
    
    texte_decision = models.TextField(default='')
    decision_original_path = models.TextField(default='')
    decision_treated_path = models.TextField(default='')
    corbeille = models.BooleanField(default=False)
    # 0 => did not be opened yet, 1 => opened but not completed yet, 2 => completely annotated
    annotation_state = models.IntegerField(default=0)
    # This is automiticaally filled when creating object i.e 
    # when uploading the decision file with the current date and time
    upload_date = models.DateTimeField(auto_now_add=True)
    # Can be considered as last modification date
    annotation_date = models.DateTimeField(auto_now=True)
    uploader_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True, related_name='%(class)s_uploader')
    annotator_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True, related_name='%(class)s_annotator')
    juridiction_id = models.ForeignKey(Juridiction,
                                on_delete=models.SET_NULL, null=True,)
    
    def __str__(self):
        return self.rg

class Personne(models.Model):
    titre = models.CharField(max_length=20, default='',)
    # nom field can be filled with person or entreprise name
    nom = models.TextField(default='')
    prenom = models.TextField(default='')
    birth_date = models.CharField(max_length=100, default='')
    zip_code = models.ForeignKey(Ville,
                                on_delete=models.SET_NULL, null=True,)
    adresse = models.TextField(default='')
    siret = models.TextField(default='')
    naf = models.TextField(default='')
    # If true so physical person, else it's an entreprise
    physique = models.BooleanField(default=True)
    # Position fields
    titre_position = models.IntegerField(default=-1)
    nom_position = models.IntegerField(default=-1)
    prenom_position = models.IntegerField(default=-1)
    birth_date_position = models.IntegerField(default=-1)
    zip_code_position = models.IntegerField(default=-1)
    adresse_position = models.IntegerField(default=-1)
    siret_position = models.IntegerField(default=-1)
    naf_position = models.IntegerField(default=-1)
    
    def __str__(self):
        return ' '.join([(self.titre + ' ' + self.prenom if self.prenom != ''  else self.siret)
                        , self.nom, self.zip_code])

class DecisionPersonne(models.Model):
    class Meta:
        unique_together = (('decision_id', 'person_id'),)
    # Did not make the primary key composed of decicion id and perosn id 
    # in case of avocat can be related to more than one person in one decision
    decision_id = models.ForeignKey(Decision,
                                on_delete=models.CASCADE,)
    person_id = models.ForeignKey(Personne,
                                on_delete=models.CASCADE, related_name='%(class)s_person')
    # Person function in this decision
    fonction = models.TextField(default='')
    # Partie id in case of avocat function (add all party ids who are associated to this avocat)
    person2_id = models.ManyToManyField(Personne,
                                null=True, related_name='%(class)s_person2')
    # In case of avocat function                            
    barreau = models.TextField(default='')
    
    # Position fields
    # fonction_position = models.IntegerField(default=-1)
    barreau_position = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.fonction

class Categorie(models.Model):
    noppac = models.CharField(max_length=50, primary_key= True)
    description = models.TextField(default='', null=True)
    # In case of avocat function                            
    objet = models.TextField( default='', null=True)
    
    def __str__(self):
        return self.description

class Demande(models.Model):

    decision_id = models.ForeignKey(Decision,
                                on_delete=models.CASCADE,)
    categorie_id = models.ForeignKey(Categorie,
                                on_delete=models.SET_NULL, null=True, related_name='%(class)s_categorie')
    montant_demande = models.DecimalField(max_digits=10, decimal_places=3, default=-1)
    unite_demande = models.CharField(max_length=20, default='', )
    quantite_demande = models.CharField(max_length=200, default='', )
    montant_resultat = models.DecimalField(max_digits=10, decimal_places=3, default=-1)
    unite_resultat = models.CharField(max_length=20, default='', )
    quantite_resultat = models.CharField(max_length=200, default='', )

    pretention = models.TextField(default='')
    dispositifs = models.TextField(default='')
    motifs = models.TextField(default='')
    # Demand result accepted or refused 
    resultat = models.BooleanField(default=True)
    # Set by the juriste when composing dataset
    default_categorie_id = models.ForeignKey(Categorie,
                                on_delete=models.SET_NULL, null=True, related_name='%(class)s_default_categorie')
    # In case the first classification of demand category was not correct
    mauvaise_categorie = models.BooleanField(default=False)
    # Position fields
    montant_demande_position = models.IntegerField(default=-1)
    unite_demande_position = models.IntegerField(default=-1)
    quantite_demande_position = models.IntegerField(default=-1)
    montant_resultat_position = models.IntegerField(default=-1)
    unite_resultat_position = models.IntegerField(default=-1)
    quantite_resultat_position = models.IntegerField(default=-1)
    pretention_position = models.IntegerField(default=-1)
    dispositifs_position = models.IntegerField(default=-1)
    motifs_position = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.categorie_id

class Demander(models.Model):
    class Meta:
        unique_together = (('demande_id', 'person_id'),)
    demande_id = models.ForeignKey(Demande,
                                on_delete=models.CASCADE,)
    # Id demandeur
    person_id = models.ForeignKey(Personne,
                                on_delete=models.CASCADE,)

class Defender(models.Model):
    class Meta:
        unique_together = (('demande_id', 'person_id'),)
    demande_id = models.ForeignKey(Demande,
                                on_delete=models.CASCADE,)
    # Id defendeur
    person_id = models.ForeignKey(Personne,
                                on_delete=models.CASCADE,)

class Norme(models.Model):

    fondement = models.TextField( default='', null=True)
    texte_norme = models.TextField(default='', null=True)
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)
    def __str__(self):
        return self.fondement

class CategorieNorme(models.Model):

    class Meta:
        unique_together = (('categorie_id', 'norme_id'),)
    
    categorie_id = models.ForeignKey(Categorie,
                                on_delete=models.CASCADE,)
    norme_id = models.ForeignKey(Norme,
                                on_delete=models.CASCADE,)
