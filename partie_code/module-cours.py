
# CLASSE MODULE

class Module:
    def __init__(self, titre, type_contenu, contenu, ordre):
        self.titre = titre
        self.type_contenu = type_contenu
        self.contenu = contenu
        self.ordre = ordre

    def afficherContenu(self):
        print(f" Module {self.ordre}: {self.titre} ({self.type_contenu})")

# CLASSE COURS

class Cours:
    compteur_id = 1  # simulation auto-increment

    def __init__(self, titre, description, niveau, duree):
        self.id_cours = Cours.compteur_id
        Cours.compteur_id += 1

        self.titre = titre
        self.description = description
        self.niveau = niveau
        self.duree = duree
        self.modules = []

    def ajouterModule(self, module):
        self.modules.append(module)

    def afficherCours(self):
        print(f"\n Cours {self.id_cours}: {self.titre}")
        print(f"   Description: {self.description}")
        print(f"   Niveau: {self.niveau} | Durée: {self.duree}h")
        print("   Modules :")

        # tri des modules par ordre
        for m in sorted(self.modules, key=lambda x: x.ordre):
            m.afficherContenu()



# SYSTEME E-LEARNING

class PlateformeElearning:
    def __init__(self):
        self.cours = []

    def ajouterCours(self, cours):
        self.cours.append(cours)

    def afficherTousLesCours(self):
        print("\n LISTE DES COURS :")
        for c in self.cours:
            c.afficherCours()

    def rechercherCours(self, mot_cle):
        print(f"\n Résultat recherche pour '{mot_cle}':")
        for c in self.cours:
            if mot_cle.lower() in c.titre.lower():
                c.afficherCours()



# TEST (simulation projet)


if __name__ == "__main__":

    plateforme = PlateformeElearning()

    #  Cours 1 
    c1 = Cours("Python", "Apprendre Python", 1, 10)
    c1.ajouterModule(Module("Variables", "video", "Intro variables", 1))
    c1.ajouterModule(Module("Boucles", "video", "For/While", 2))
    c1.ajouterModule(Module("Conditions", "texte", "If/Else", 3))

    #  Cours 2 
    c2 = Cours("Java", "Programmation orientée objet", 2, 15)
    c2.ajouterModule(Module("Classes", "video", "POO", 1))
    c2.ajouterModule(Module("Héritage", "texte", "Concept", 2))

    #  Cours 3 
    c3 = Cours("SQL", "Base de données", 1, 12)
    c3.ajouterModule(Module("SELECT", "texte", "Requête", 1))
    c3.ajouterModule(Module("JOIN", "video", "Jointures", 2))

    # Ajout à la plateforme
    plateforme.ajouterCours(c1)
    plateforme.ajouterCours(c2)
    plateforme.ajouterCours(c3)

    # Affichage
    plateforme.afficherTousLesCours()

    # Recherche
    plateforme.rechercherCours("Python")
