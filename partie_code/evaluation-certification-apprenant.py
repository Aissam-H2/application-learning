from datetime import date
import uuid


class Evaluation:
    def __init__(self, id_evaluation, date_passation, reponses):
        self.id_evaluation = id_evaluation
        self.date_passation = date_passation
        self.reponses = reponses  # dictionnaire {question: réponse}
        self.score = 0.0
        self.commentaire = ""

    def calculer_score(self, bonnes_reponses):
        """
        bonnes_reponses : dict {question: bonne réponse}
        """
        total = len(bonnes_reponses)
        correct = 0

        for q, rep in self.reponses.items():
            if q in bonnes_reponses and bonnes_reponses[q] == rep:
                correct += 1

        self.score = (correct / total) * 100 if total > 0 else 0
        return self.score

    def generer_feedback(self):
        if self.score >= 80:
            self.commentaire = "Excellent travail !"
        elif self.score >= 50:
            self.commentaire = "Bon effort, continuez."
        else:
            self.commentaire = "Besoin d'amélioration."

        return self.commentaire


class Certification:
    def __init__(self, id_certificat, date_emission):
        self.id_certificat = id_certificat
        self.date_emission = date_emission
        self.code_validation = self._generer_code()

    def _generer_code(self):
        return str(uuid.uuid4())

    def generer_pdf(self):
        
        return f"Certificat {self.id_certificat} généré en PDF."

    def verifier_authenticite(self, code):
        return self.code_validation == code


class Apprenant:
    def __init__(self, nom, niveau_etude, objectif):
        self.nom = nom
        self.niveau_etude = niveau_etude
        self.objectif = objectif
        self.parcours_suivis = []
        self.progression = {}
        self.evaluations = []
        self.certifications = []

    def passer_evaluation(self, evaluation):
        self.evaluations.append(evaluation)
        print(f"{self.nom} a passé l'évaluation {evaluation.id_evaluation}")

    def consulter_recommandations(self):
        
        return f"Recommandations basées sur le niveau {self.niveau_etude}"

    def telecharger_certificat(self, certification):
        if certification in self.certifications:
            return certification.generer_pdf()
        return "Certificat non trouvé"

    def obtenir_certification(self, evaluation):
        """
        Génère une certification si score >= 50
        """
        if evaluation.score >= 50:
            certif = Certification(
                id_certificat=len(self.certifications) + 1,
                date_emission=date.today()
            )
            self.certifications.append(certif)
            return certif
        else:
            print("Score insuffisant pour obtenir une certification.")
            return None