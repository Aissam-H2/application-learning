from datetime import date

class Utilisateur:
    def __init__(self, id, nom, prenom, date_naissance, email, mot_de_passe):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.date_inscription = date.today()
            
        
    def sinscrire(self):
        # Méthode pour s'inscrire
        for u in utilisateurs:
            if u.email == self.email:
                print("Email déjà utilisé ")
                return

        # Ajouter utilisateur
        utilisateurs.append(self)

        print(f"{self.nom} inscrit avec succès ")

    # Méthode pour se connecter
    def seConnecter(self, email, mot_de_passe):
        if self.email == email and self.mot_de_passe == mot_de_passe:
            print("Connexion réussie ")
            return True
        else:
            print("Email ou mot de passe incorrect ")
            return False

    # Méthode pour modifier le profil
    def modifierProfil(self, nom=None, prenom=None, email=None, mot_de_passe=None):
        if nom:
            self.nom = nom
        if prenom:
            self.prenom = prenom
        if email:
            self.email = email
        if mot_de_passe:
            self.mot_de_passe = mot_de_passe

        print("Profil mis à jour avec succès ")
