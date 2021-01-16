from django.db import models

class PersonnePhysique(models.Model):
    nom_personne_ph = models.CharField(max_length=50) #, help_text='Nom')
    position_nom_personne_ph = models.IntegerField()
    prenom_personne_ph = models.CharField(max_length=50)
    position_prenom_personne_ph = models.IntegerField()
    titre_personne_ph = models.CharField(max_length=20, blank=True)
    position_titre_personne_ph = models.IntegerField()
    date_naissance_personne_ph = models.DateField(blank=True)
    position_date_naissance = models.IntegerField()
    adresse_personne_ph = models.CharField(max_length=255, blank=True)
    position_adresse_personne_ph = models.IntegerField(blank=True)
    code_postale_personne_ph = models.ForeignKey('Ville', on_delete=models.CASCADE)
    barreau = models.CharField(max_length=255, blank=True)
    position_barreau = models.IntegerField()
    pseudo_personne_ph = models.CharField(max_length=50, blank=True)
    sexe_personne_ph = models.BooleanField()
    fonction = models.ForeignKey('Fonction', on_delete=models.CASCADE,)
    def __str__(self):
        return ' '.join([self.titre_personne_ph, 
                        self.nom_personne_ph, 
                        self.prenom_personne_ph])

class PersonneMorale(models.Model):
    nom_entreprise = models.CharField(max_length=50)
    position_nom_entreprise = models.IntegerField()
    numero_SIRET = models.CharField(max_length=50)
    position_numero_SIRET = models.IntegerField()
    numero_NAF = models.CharField(max_length=50, blank=True)
    position_numero_NAF = models.IntegerField()
    pseudo_entreprise = models.CharField(max_length=50, blank=True)
    adresse_entreprise = models.CharField(max_length=255, blank=True)
    position_adresse_entreprise = models.IntegerField()
    code_postale_entreprise = models.ForeignKey('Ville', on_delete=models.CASCADE)
    fonction = models.ForeignKey('Fonction', on_delete=models.CASCADE,)

class Fonction(models.Model):
    nom_fonction = models.CharField(max_length=50)

class Decision(models.Model):
    texte_decision = models.TextField()
    numero_rg = models.CharField(max_length=30)
    position_numero_rg = models.IntegerField()
    date_decision = models.DateField(blank=True)
    position_date_decision = models.IntegerField(blank=True)
    chambre = models.CharField(max_length=100, blank=True)
    position_chambre = models.IntegerField()
    chemin_fichier = models.TextField(blank=True)
    juridiction = models.ForeignKey('Juridiction', on_delete=models.CASCADE)

class Juridiction(models.Model):
    type_juridiction = models.CharField(max_length=255)
    position_type_juridiction = models.IntegerField()
    code_postale_juridiction = models.ForeignKey('Ville', on_delete=models.CASCADE)
    abbreviation_type = models.CharField(max_length=20, blank=True)

class Demande(models.Model):
    # Pretention, Motifs and dispos
    pretention = models.TextField(blank=True)
    position_pretention = models.IntegerField(blank=True)
    motifs = models.TextField(blank=True)
    position_motifs = models.IntegerField(blank=True)
    dispositifs = models.TextField(blank=True)
    position_dispositifs = models.IntegerField(blank=True)
    # Demande
    montant_demande = models.CharField(max_length=50, blank=True)
    position_montant_demande = models.IntegerField(blank=True)
    unite_demande = models.CharField(max_length=50, blank=True)
    position_unite_demande = models.IntegerField(blank=True)
    quantite_demande = models.CharField(max_length=255, blank=True)
    position_quantite_demande = models.IntegerField(blank=True)
    # Result
    montant_resultat = models.CharField(max_length=50, blank=True)
    position_montant_resultat = models.IntegerField(blank=True)
    unite_resultat = models.CharField(max_length=50, blank=True)
    position_unite_resultat = models.IntegerField(blank=True)
    quantite_resultat = models.CharField(max_length=255, blank=True)
    position_quantite_resultat = models.IntegerField(blank=True)
    result = models.BooleanField()
    # Decision many (demandes) to one (decision)
    id_decision = models.ForeignKey('Decision', on_delete=models.CASCADE)
    # Demande Categorie
    noppac = models.ForeignKey('CategorieDemande', on_delete=models.CASCADE)

class CategorieDemande(models.Model):
    noppac = models.CharField(primary_key=True, max_length=255)
    descriptif_categorie = models.TextField(blank=True)
    objet_categorie = models.TextField(blank=True)
    normes = models.ManyToManyField('Norme')
    
class Norme(models.Model):
    fondement = models.TextField(blank=True)
    texte_norme = models.TextField(blank=True)
    date_debut = models.DateField(blank=True)
    date_fin = models.DateField(blank=True)
    
class Ville(models.Model):
    code_postale = models.CharField(max_length=10, primary_key=True)
    ville = models.CharField(max_length=255)

# 2 problems : avocats + 2 IDs uniques
class PersonneDecision(models.Model):
    class Meta:
        unique_together = [
                            ['id_decision', 'id_personne_ph'],
                            ['id_decision', 'id_personne_morale'],
                        ]
    id_decision = models.ForeignKey('Decision', 
                            on_delete=models.CASCADE)

    id_personne_ph = models.ForeignKey('PersonnePhysique', 
                            on_delete=models.CASCADE, blank=True)

    id_personne_morale = models.ForeignKey('PersonneMorale', 
                            on_delete=models.CASCADE, blank=True)

    id_fonction = models.ForeignKey('Fonction', 
                            on_delete=models.CASCADE)

    position_fonction = models.IntegerField(blank=True)

class PartieDemande(models.Model):
    class Meta:
        unique_together = [
                            ['id_demande', 'id_demandeur']
                        ]
    id_demande = models.ForeignKey('Demande', on_delete=models.CASCADE)
    id_demandeur = models.ForeignKey('PersonnePhysique', on_delete=models.CASCADE)
    #id_defendeur = models.ForeignKey('PersonnePhysique', on_delete=models.CASCADE)

class Annotateur(models.Model):
    pass

class Annotation(models.Model):
    pass


    