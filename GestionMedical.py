import pickle
import os

class Patient:
    nbr_patients = 0

    def __init__(self, nom, age, poids, taille, pression, diabetique):
        self.__nom = nom
        self.__age = age
        self.__poids = poids
        self.__taille = taille
        self.__pression = pression
        self.__diabetique = diabetique
        Patient.nbr_patients += 1

    def __str__(self):
        if self.__diabetique:
            return f"Le patient {self.__nom} de {self.__age} ans, il pèse {self.__poids} kg et mesure {self.__taille} cm. Il est diabétique et il a {self.__pression} mmHg de pression."
        else:
            return f"Le patient {self.__nom} de {self.__age} ans, il pèse {self.__poids} kg et mesure {self.__taille} cm. Il n'est pas diabétique et il a {self.__pression} mmHg de pression."

    def getNom(self):
        return self.__nom

    def getAge(self):
        return self.__age

    def getPoids(self):
        return self.__poids

    def getTaille(self):
        return self.__taille

    def getPression(self):
        return self.__pression

    def getDiabetique(self):
        return self.__diabetique

    def setDiabetique(self, valeur):
        self.__diabetique = valeur

    def setPoids(self, valeur):
        if 1.5 <= valeur < 400:
            self.__poids = valeur
        else:
            print("Erreur : Le poids doit être compris entre 1.5 et 400 kg.")

    def setTaille(self, valeur):
        if 25 <= valeur < 220:
            self.__taille = valeur
        else:
            print("Erreur : La taille doit être comprise entre 25 et 220 cm.")

    def setAge(self, valeur):
        if valeur > 0:
            self.__age = valeur
        else:
            print("Erreur : L'âge doit être un nombre positif.")

    def setPression(self, valeur):
        if 40 <= valeur <= 250:
            self.__pression = valeur
        else:
            print("Erreur : La pression doit être comprise entre 40 et 250 mmHg.")

    def IMC(self):
        return self.__poids / (self.__taille / 100) ** 2

    def score(self):
        s = 0
        if self.IMC() < 18.5:
            s += 2
        elif 25 <= self.IMC() <= 29.9:
            s += 1
        elif self.IMC() >= 30:
            s += 3

        if 40 <= self.__age <= 60:
            s += 2
        elif self.__age > 60:
            s += 4

        if 120 <= self.__pression <= 139:
            s += 2
        elif self.__pression >= 140:
            s += 4

        if self.__diabetique:
            s += 5

        return s

    @staticmethod
    def comparer(p1, p2):
        return p1.score() > p2.score()

    @staticmethod
    def trier(patients):
        test = True
        while test:
            test = False
            for i in range(len(patients) - 1):
                if Patient.comparer(patients[i], patients[i + 1]):
                    patients[i], patients[i + 1] = patients[i + 1], patients[i]
                    test = True
        return patients

    @classmethod
    def nombre_total(cls):
        return cls.nbr_patients

    @staticmethod
    def comparer_imcs(p1, p2):
        imc1 = p1.IMC()
        imc2 = p2.IMC()
        if imc1 > imc2:
            return "L'état du premier patient est plus grave."
        elif imc1 < imc2:
            return "L'état du deuxième patient est plus grave."
        else:
            return "Les patients sont identiques."

    @classmethod
    def supprimer_patient(cls):
        if cls.nbr_patients > 0:
            cls.nbr_patients -= 1


class Medecin:
    nbr_medecins = 0

    def __init__(self, nom, specialite, inpe, chirurgient, service, grade):
        self.__nom = nom
        self.__specialite = specialite
        self.__inpe = inpe
        self.__chirurgient = chirurgient
        self.__service = service
        self.__grade = grade
        Medecin.nbr_medecins += 1

    def __str__(self):
        if self.__chirurgient:
            return f"Le médecin {self.__nom} de spécialité {self.__specialite}, de grade {self.__grade}, il possède l'INPE {self.__inpe}. Il est chirurgien et il pratique dans le service {self.__service}."
        else:
            return f"Le médecin {self.__nom} de spécialité {self.__specialite}, de grade {self.__grade}, il possède l'INPE {self.__inpe}. Il pratique dans le service {self.__service}."

    def getNom(self):
        return self.__nom

    def getSpecialite(self):
        return self.__specialite

    def getInpe(self):
        return self.__inpe

    def getChirurgient(self):
        return self.__chirurgient

    def getService(self):
        return self.__service

    def getGrade(self):
        return self.__grade

    def setChirurgien(self, valeur):
        self.__chirurgient = valeur

    def setService(self, valeur):
        self.__service = valeur

    def setGrade(self, valeur):
        self.__grade = valeur

    @classmethod
    def nombre_total(cls):
        return cls.nbr_medecins

    @classmethod
    def supprimer_medecin(cls):
        if cls.nbr_medecins > 0:
            cls.nbr_medecins -= 1


class Consultation:
    nbr_consultations = 0

    def __init__(self, patient, medecin, date, note):
        self.__patient = patient
        self.__medecin = medecin
        self.__date = date
        self.__note = note
        Consultation.nbr_consultations += 1

    def __str__(self):
        return f"Consultation effectuée le {self.__date} par Dr {self.__medecin.getNom()} pour le patient {self.__patient.getNom()}."

    def getMedecin(self):
        return self.__medecin

    def getPatient(self):
        return self.__patient

    def getDate(self):
        return self.__date

    def getNote(self):
        return self.__note

    def ajouterNote(self, valeur):
        self.__note.append(valeur)

    @classmethod
    def nombre_total(cls):
        return cls.nbr_consultations


def ChargementMedecins():
    try:
        with open("medecins.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Aucun fichier de médecins trouvé. Création d'une nouvelle liste.")
        return []
    except EOFError:
        print("Fichier de médecins vide. Création d'une nouvelle liste.")
        return []


def SauvegardeMedecins(medecins):
    with open("medecins.pkl", "wb") as file:
        pickle.dump(medecins, file)


def ChargementPatients():
    try:
        with open("patients.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Aucun fichier de patients trouvé. Création d'une nouvelle liste.")
        return []
    except EOFError:
        print("Fichier de patients vide. Création d'une nouvelle liste.")
        return []


def SauvegardePatients(patients):
    with open("patients.pkl", "wb") as file:
        pickle.dump(patients, file)


def ChargementConsultations():
    try:
        with open("consultations.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Aucun fichier de consultations trouvé. Création d'une nouvelle liste.")
        return []
    except EOFError:
        print("Fichier de consultations vide. Création d'une nouvelle liste.")
        return []


def SauvegardeConsultations(consultations):
    with open("consultations.pkl", "wb") as file:
        pickle.dump(consultations, file)


def Menu():
    global patients, medecins, consultations
    os.system('cls')
    print("Bonjour!")
    print("1- Gestion des Patients")
    print("2- Gestion des Médecins")
    print("3- Gestion des Consultations")
    print("4- Quitter l'application")
    option = input("Veuillez choisir le volet de gestion : ")
    if option == "1":
        GestionPatients()
    elif option == "2":
        GestionMedecins()
    elif option == "3":
        GestionConsultations()
    elif option == "4":
        SauvegardePatients(patients)
        SauvegardeMedecins(medecins)
        SauvegardeConsultations(consultations)
        print("Merci d'avoir utilisé l'application. À bientôt !")
        return
    else:
        print("Option invalide. Veuillez réessayer.")
        Menu()


def GestionPatients():
    os.system('cls')
    print("Gestion des Patients")
    print("1- Afficher tous les patients")
    print("2- Ajouter un patient")
    print("3- Chercher un patient")
    print("4- Supprimer un patient")
    print("5- Revenir au menu principal")
    option = input("Choisissez une option : ")
    if option == "1":
        AfficherPatients()
    elif option == "2":
        AjouterPatient()
    elif option == "3":
        ChercherPatient()
    elif option == "4":
        SupprimerPatient()
    elif option == "5":
        Menu()
    else:
        print("Option invalide. Veuillez réessayer.")
        GestionPatients()


def AfficherPatients():
    os.system('cls')
    if not patients:
        print("Aucun patient enregistré.")
    else:
        for i, patient in enumerate(patients):
            print(f"{i + 1}- {patient}")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionPatients()


def AjouterPatient():
    os.system('cls')
    print("Ajouter un nouveau patient")
    nom = input("Nom : ")
    try:
        age = int(input("Âge : "))
        poids = float(input("Poids (kg) : "))
        taille = float(input("Taille (cm) : "))
        pression = int(input("Pression artérielle (mmHg) : "))
        diabetique = input("Diabétique (Oui/Non) : ").lower() == "oui"
        nouveau_patient = Patient(nom, age, poids, taille, pression, diabetique)
        patients.append(nouveau_patient)
        print(f"Le patient {nom} a été ajouté avec succès.")
    except ValueError:
        print("Erreur : Veuillez entrer des valeurs valides.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionPatients()


def ChercherPatient():
    os.system('cls')
    print("Chercher un patient")
    nom = input("Entrez le nom du patient : ")
    for patient in patients:
        if patient.getNom().lower() == nom.lower():
            print(patient)
            input("\nAppuyez sur Entrée pour revenir au menu précédent.")
            GestionPatients()
            return
    print("Aucun patient trouvé avec ce nom.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionPatients()


def SupprimerPatient():
    os.system('cls')
    print("Supprimer un patient")
    nom = input("Entrez le nom du patient à supprimer : ")
    for patient in patients:
        if patient.getNom().lower() == nom.lower():
            patients.remove(patient)
            Patient.supprimer_patient()
            print(f"Le patient {nom} a été supprimé avec succès.")
            input("\nAppuyez sur Entrée pour revenir au menu précédent.")
            GestionPatients()
            return
    print("Aucun patient trouvé avec ce nom.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionPatients()


def GestionMedecins():
    os.system('cls')
    print("Gestion des Médecins")
    print("1- Afficher tous les médecins")
    print("2- Ajouter un médecin")
    print("3- Chercher un médecin")
    print("4- Supprimer un médecin")
    print("5- Revenir au menu principal")
    option = input("Choisissez une option : ")
    if option == "1":
        AfficherMedecins()
    elif option == "2":
        AjouterMedecin()
    elif option == "3":
        ChercherMedecin()
    elif option == "4":
        SupprimerMedecin()
    elif option == "5":
        Menu()
    else:
        print("Option invalide. Veuillez réessayer.")
        GestionMedecins()


def AfficherMedecins():
    os.system('cls')
    if not medecins:
        print("Aucun médecin enregistré.")
    else:
        for i, medecin in enumerate(medecins):
            print(f"{i + 1}- {medecin}")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionMedecins()


def AjouterMedecin():
    os.system('cls')
    print("Ajouter un nouveau médecin")
    nom = input("Nom : ")
    specialite = input("Spécialité : ")
    inpe = input("INPE : ")
    chirurgient = input("Chirurgien (Oui/Non) : ").lower() == "oui"
    service = input("Service : ")
    grade = input("Grade : ")
    nouveau_medecin = Medecin(nom, specialite, inpe, chirurgient, service, grade)
    medecins.append(nouveau_medecin)
    print(f"Le médecin {nom} a été ajouté avec succès.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionMedecins()


def ChercherMedecin():
    os.system('cls')
    print("Chercher un médecin")
    nom = input("Entrez le nom du médecin : ")
    for medecin in medecins:
        if medecin.getNom().lower() == nom.lower():
            print(medecin)
            input("\nAppuyez sur Entrée pour revenir au menu précédent.")
            GestionMedecins()
            return
    print("Aucun médecin trouvé avec ce nom.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionMedecins()


def SupprimerMedecin():
    os.system('cls')
    print("Supprimer un médecin")
    nom = input("Entrez le nom du médecin à supprimer : ")
    for medecin in medecins:
        if medecin.getNom().lower() == nom.lower():
            medecins.remove(medecin)
            Medecin.supprimer_medecin()
            print(f"Le médecin {nom} a été supprimé avec succès.")
            input("\nAppuyez sur Entrée pour revenir au menu précédent.")
            GestionMedecins()
            return
    print("Aucun médecin trouvé avec ce nom.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionMedecins()


def GestionConsultations():
    os.system('cls')
    print("Gestion des Consultations")
    print("1- Afficher toutes les consultations")
    print("2- Ajouter une consultation")
    print("3- Chercher une consultation")
    print("4- Revenir au menu principal")
    option = input("Choisissez une option : ")
    if option == "1":
        AfficherConsultations()
    elif option == "2":
        AjouterConsultation()
    elif option == "3":
        ChercherConsultation()
    elif option == "4":
        Menu()
    else:
        print("Option invalide. Veuillez réessayer.")
        GestionConsultations()


def AfficherConsultations():
    os.system('cls')
    if not consultations:
            print("Aucune consultation enregistrée.")
    else:
        for i, consultation in enumerate(consultations):
            print(f"{i + 1}- {consultation}")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionConsultations()


def AjouterConsultation():
    os.system('cls')
    print("Ajouter une nouvelle consultation")
    if not patients or not medecins:
        print("Veuillez d'abord ajouter des patients et des médecins.")
        input("\nAppuyez sur Entrée pour revenir au menu précédent.")
        GestionConsultations()
        return

    print("Liste des patients :")
    for i, patient in enumerate(patients):
        print(f"{i + 1}- {patient.getNom()}")
    try:
        patient_index = int(input("Choisissez un patient (numéro) : ")) - 1
        if patient_index < 0 or patient_index >= len(patients):
            raise ValueError("Numéro de patient invalide.")
    except ValueError as e:
        print(f"Erreur : {e}")
        input("\nAppuyez sur Entrée pour revenir au menu précédent.")
        GestionConsultations()
        return

    print("Liste des médecins :")
    for i, medecin in enumerate(medecins):
        print(f"{i + 1}- {medecin.getNom()}")
    try:
        medecin_index = int(input("Choisissez un médecin (numéro) : ")) - 1
        if medecin_index < 0 or medecin_index >= len(medecins):
            raise ValueError("Numéro de médecin invalide.")
    except ValueError as e:
        print(f"Erreur : {e}")
        input("\nAppuyez sur Entrée pour revenir au menu précédent.")
        GestionConsultations()
        return

    date = input("Date de la consultation (JJ/MM/AAAA) : ")
    note = input("Note de la consultation : ")
    nouvelle_consultation = Consultation(patients[patient_index], medecins[medecin_index], date, note)
    consultations.append(nouvelle_consultation)
    print("La consultation a été ajoutée avec succès.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionConsultations()


def ChercherConsultation():
    os.system('cls')
    print("Chercher une consultation")
    date = input("Entrez la date de la consultation (JJ/MM/AAAA) : ")
    for consultation in consultations:
        if consultation.getDate() == date:
            print(consultation)
            input("\nAppuyez sur Entrée pour revenir au menu précédent.")
            GestionConsultations()
            return
    print("Aucune consultation trouvée à cette date.")
    input("\nAppuyez sur Entrée pour revenir au menu précédent.")
    GestionConsultations()


patients = ChargementPatients()
medecins = ChargementMedecins()
consultations = ChargementConsultations()

Menu()

SauvegardePatients(patients)
SauvegardeMedecins(medecins)
SauvegardeConsultations(consultations)