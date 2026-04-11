from datetime import datetime

# class enseignant
class Enseignant:
    
    def __init__(self, id, nom, prenom, email, specialite):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.specialite = specialite
        self.biographie = ""
        self.date_inscription = datetime.now()
        self.cours_crees = []
    
    def creer_cours(self, titre, description, niveau_difficulte, duree):
        cours = {
            'id': len(self.cours_crees) + 1,
            'titre': titre,
            'description': description,
            'niveau_difficulte': niveau_difficulte,
            'duree': duree,
            'date_creation': datetime.now()
        }
        self.cours_crees.append(cours)
        return cours
    
    def evaluer_apprenant(self, apprenant, score, commentaire=""):
        evaluation = {
            'apprenant': apprenant,
            'score': score,
            'commentaire': commentaire,
            'date': datetime.now(),
            'valide': score >= 10
        }
        return evaluation
    
    def generer_rapport(self):
        rapport = {
            'nom': f"{self.prenom} {self.nom}",
            'email': self.email,
            'specialite': self.specialite,
            'date_inscription': self.date_inscription,
            'biographie': self.biographie,
            'nombre_cours': len(self.cours_crees),
            'cours': self.cours_crees
        }
        return rapport
    
    def ajouter_biographie(self, biographie):
        self.biographie = biographie
    
    def supprimer_cours(self, id_cours):
        for i, cours in enumerate(self.cours_crees):
            if cours['id'] == id_cours:
                del self.cours_crees[i]
                return True
        return False
    def afficher_infos(self):
        print(f"ID: {self.id}")
        print(f"Nom: {self.nom} {self.prenom}")
        print(f"Email: {self.email}")
        print(f"Spécialité: {self.specialite}")
        print(f"Biographie: {self.biographie if self.biographie else 'Non renseignée'}")
        print(f"Date inscription: {self.date_inscription.strftime('%d/%m/%Y')}")
        print(f"Nombre de cours créés: {len(self.cours_crees)}")
        
        if self.cours_crees:
            print("\nListe des cours:")
            for cours in self.cours_crees:
                print(f"  - {cours['titre']} (Niveau: {cours['niveau_difficulte']}, Durée: {cours['duree']}h)")
    
    def modifier_cours(self, id_cours, **kwargs):
        for cours in self.cours_crees:
            if cours['id'] == id_cours:
                for key, value in kwargs.items():
                    if key in cours:
                        cours[key] = value
                return True
        return False
class Administrateur:    
    def __init__(self, id, nom, prenom, email, niveau_acces):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.niveau_acces = niveau_acces
        self.date_inscription = datetime.now()
        self.utilisateurs_geres = []
        self.logs = []
    
    def gerer_utilisateurs(self, utilisateur, action):
        if action == "creer":
            self.utilisateurs_geres.append(utilisateur)
            self._ajouter_log(f"Utilisateur {utilisateur.email} créé")
            return True
        elif action == "supprimer":
            for i, u in enumerate(self.utilisateurs_geres):
                if u.email == utilisateur.email:
                    del self.utilisateurs_geres[i]
                    self._ajouter_log(f"Utilisateur {utilisateur.email} supprimé")
                    return True
            return False
        elif action == "modifier":
            self._ajouter_log(f"Utilisateur {utilisateur.email} modifié")
            return True
        return False
    
    def configurer_systeme(self, parametre, valeur):
        configuration = {
            'parametre': parametre,
            'valeur': valeur,
            'date': datetime.now()
        }
        self._ajouter_log(f"Système configuré: {parametre} = {valeur}")
        return configuration
    
    def voir_logs(self):
        return self.logs
    
    def afficher_infos(self):
        print(f"ID: {self.id}")
        print(f"Nom: {self.nom} {self.prenom}")
        print(f"Email: {self.email}")
        print(f"Niveau d'accès: {self.niveau_acces}")
        print(f"Date inscription: {self.date_inscription.strftime('%d/%m/%Y')}")
        print(f"Utilisateurs gérés: {len(self.utilisateurs_geres)}")
        
        if self.utilisateurs_geres:
            print("\nListe des utilisateurs gérés:")
            for user in self.utilisateurs_geres:
                print(f"  - {user.prenom} {user.nom} ({user.email})")
        
        if self.logs:
            print(f"\nDerniers logs ({len(self.logs)} au total):")
            for log in self.logs[-5:]:
                print(f"  - {log}")
    
    def afficher_statistiques(self):
        stats = {
            'total_utilisateurs': len(self.utilisateurs_geres),
            'date': datetime.now(),
            'admin_nom': f"{self.prenom} {self.nom}"
        }
        
        print(f" Admin : {stats['admin_nom']}")
        print(f"Total utilisateurs gérés: {stats['total_utilisateurs']}")
        print(f"Date: {stats['date'].strftime('%d/%m/%Y %H:%M')}")
        return stats
    
    def _ajouter_log(self, message):
        log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        self.logs.append(log)
class Exercice:  
    def __init__(self, id_exercice, type_exercice, enonce, difficulte, score_minimum):
        self.id_exercice = id_exercice
        self.type = type_exercice
        self.enonce = enonce
        self.difficulte = difficulte
        self.score_minimum = score_minimum
        self.reponse_correcte = None
        self.module = None
        self.soumissions = []
        self.date_creation = datetime.now()
    
    def definir_reponse(self, reponse):
        self.reponse_correcte = reponse
        return True
    
    def valider(self, reponse, apprenant):
        est_correct = (reponse == self.reponse_correcte) if self.reponse_correcte else False
        score_obtenu = self.score_minimum if est_correct else 0
        
        soumission = {
            'apprenant': apprenant,
            'reponse': reponse,
            'score': score_obtenu,
            'date': datetime.now(),
            'correct': est_correct
        }
        
        self.soumissions.append(soumission)
        return soumission
    
    def associer_module(self, module):
        self.module = module
        return True
    
    def afficher_infos(self):
        print(f"ID Exercice: {self.id_exercice}")
        print(f"Type: {self.type}")
        print(f"Difficulté: {'⭐' * self.difficulte}")
        print(f"Score minimum: {self.score_minimum}")
        print(f"Énoncé: {self.enonce}")
        print(f"Date création: {self.date_creation.strftime('%d/%m/%Y')}")
        
        if self.module:
            print(f"Module associé: {self.module}")
        
        print(f"Nombre de soumissions: {len(self.soumissions)}")
        
        if self.soumissions:
            print("\nDernières soumissions:")
            for sub in self.soumissions[-3:]:
                status = "" if sub['correct'] else "❌"
                print(f"  {status} {sub['apprenant']} - Score: {sub['score']}")
    
    def get_statistiques(self):
        if not self.soumissions:
            return {
                'total_soumissions': 0,
                'taux_reussite': 0,
                'score_moyen': 0
            }
        
        total = len(self.soumissions)
        reussites = sum(1 for s in self.soumissions if s['correct'])
        scores = [s['score'] for s in self.soumissions]
        
        stats = {
            'total_soumissions': total,
            'taux_reussite': (reussites / total) * 100,
            'score_moyen': sum(scores) / len(scores),
            'meilleur_score': max(scores),
            'pire_score': min(scores)
        }
        return stats
    
    def modifier_enonce(self, nouvel_enonce):
        self.enonce = nouvel_enonce
        return True
    
    def modifier_difficulte(self, nouvelle_difficulte):
        if 1 <= nouvelle_difficulte <= 5:
            self.difficulte = nouvelle_difficulte
            return True
        return False
# main

