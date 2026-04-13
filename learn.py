users = []
courses = []


def creer_utilisateur(nom, email, role):
    user = {
        "id": len(users) + 1,
        "nom": nom,
        "email": email,
        "role": role
    }
    users.append(user)
    print("Utilisateur créé avec succès")


def afficher_utilisateurs():
    print("\n--- Liste des utilisateurs ---")
    for u in users:
        print(f"{u['id']} - {u['nom']} ({u['role']})")


def afficher_etudiants_global():
    print("\n--- Tous les étudiants ---")
    for u in users:
        if u["role"] == "etudiant":
            print(f"{u['id']} - {u['nom']} ({u['email']})")



def creer_cours(titre, description, professeur):
    cours = {
        "id": len(courses) + 1,
        "titre": titre,
        "description": description,
        "professeur": professeur,
        "etudiants": [],
        "lecons": [],
        "devoirs": []
    }
    courses.append(cours)
    print("Cours créé avec succès")


def afficher_cours():
    print("\n--- Liste des cours ---")
    for c in courses:
        print(f"{c['id']} - {c['titre']} (Prof: {c['professeur']})")



def affecter_etudiant(cours_id, user_id):
    cours = None
    etudiant = None

   
    for c in courses:
        if c["id"] == cours_id:
            cours = c

    
    for u in users:
        if u["id"] == user_id and u["role"] == "etudiant":
            etudiant = u

    if cours is None:
        print("Cours introuvable")
        return

    if etudiant is None:
        print("Etudiant introuvable")
        return

    
    if etudiant["nom"] in cours["etudiants"]:
        print("Etudiant déjà inscrit")
        return

    cours["etudiants"].append(etudiant["nom"])
    print("Etudiant affecté au cours avec succès")



def afficher_etudiants_cours(cours_id):
    for c in courses:
        if c["id"] == cours_id:
            print(f"\n--- Etudiants dans {c['titre']} ---")
            if not c["etudiants"]:
                print("Aucun étudiant")
            for e in c["etudiants"]:
                print(f"- {e}")
            return
    print("Cours introuvable")



def ajouter_lecon(cours_id, titre, video):
    for c in courses:
        if c["id"] == cours_id:
            c["lecons"].append({"titre": titre, "video": video})
            print("Leçon ajoutée")
            return
    print("Cours introuvable")



def creer_devoir(cours_id, titre, date_limite):
    for c in courses:
        if c["id"] == cours_id:
            c["devoirs"].append({
                "titre": titre,
                "date_limite": date_limite,
                "soumissions": []
            })
            print("Devoir créé")
            return
    print("Cours introuvable")


def soumettre_devoir(cours_id, titre_devoir, etudiant, fichier):
    for c in courses:
        if c["id"] == cours_id:
            for d in c["devoirs"]:
                if d["titre"] == titre_devoir:
                    d["soumissions"].append({
                        "etudiant": etudiant,
                        "fichier": fichier,
                        "note": None
                    })
                    print("Devoir soumis")
                    return
    print("Erreur soumission")


def noter_devoir(cours_id, titre_devoir, etudiant, note):
    for c in courses:
        if c["id"] == cours_id:
            for d in c["devoirs"]:
                if d["titre"] == titre_devoir:
                    for s in d["soumissions"]:
                        if s["etudiant"] == etudiant:
                            s["note"] = note
                            print("Note ajoutée")
                            return
    print("Erreur notation")



def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Créer utilisateur")
        print("2. Afficher utilisateurs")
        print("3. Créer cours")
        print("4. Afficher cours")
        print("5. Affecter étudiant à un cours")
        print("6. Voir étudiants d'un cours")
        print("7. Voir tous les étudiants")
        print("8. Ajouter leçon")
        print("9. Créer devoir")
        print("10. Soumettre devoir")
        print("11. Noter devoir")
        print("0. Quitter")

        choix = input("Choix: ")

        if choix == "1":
            nom = input("Nom: ")
            email = input("Email: ")
            role = input("Role (prof/etudiant): ")
            creer_utilisateur(nom, email, role)

        elif choix == "2":
            afficher_utilisateurs()

        elif choix == "3":
            titre = input("Titre: ")
            desc = input("Description: ")
            prof = input("Professeur: ")
            creer_cours(titre, desc, prof)

        elif choix == "4":
            afficher_cours()

        elif choix == "5":
            afficher_cours()
            afficher_etudiants_global()
            cid = int(input("ID cours: "))
            uid = int(input("ID étudiant: "))
            affecter_etudiant(cid, uid)

        elif choix == "6":
            afficher_cours()
            cid = int(input("ID cours: "))
            afficher_etudiants_cours(cid)

        elif choix == "7":
            afficher_etudiants_global()

        elif choix == "8":
            cid = int(input("ID cours: "))
            titre = input("Titre leçon: ")
            video = input("Vidéo: ")
            ajouter_lecon(cid, titre, video)

        elif choix == "9":
            cid = int(input("ID cours: "))
            titre = input("Titre devoir: ")
            date = input("Date limite: ")
            creer_devoir(cid, titre, date)

        elif choix == "10":
            cid = int(input("ID cours: "))
            devoir = input("Titre devoir: ")
            etu = input("Nom étudiant: ")
            fichier = input("Fichier: ")
            soumettre_devoir(cid, devoir, etu, fichier)

        elif choix == "11":
            cid = int(input("ID cours: "))
            devoir = input("Titre devoir: ")
            etu = input("Nom étudiant: ")
            note = float(input("Note: "))
            noter_devoir(cid, devoir, etu, note)

        elif choix == "0":
            print("Au revoir ")
            break

        else:
            print("Choix invalide")
