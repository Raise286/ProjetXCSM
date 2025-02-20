import pymongo
import fitz  # PyMuPDF
import re


# Fonction pour se connecter à la base de données MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Remplace l'URL de connexion si nécessaire
    db = client["Documents"]  # Accéder à la base de données "Documents"
    return db["notions"]  # Accéder à la collection "notions"


# Fonction pour sauvegarder les notions dans la base de données
def save_notion_to_db(notion_data):
    collection = connect_to_mongodb()
    collection.insert_one(notion_data)  # Insère la notion dans la collection


# Fonction pour extraire le texte d'un fichier PDF
def extract_clean_text(pdf_path):
    """
    Extrait le texte brut d'un fichier PDF et supprime les occurrences répétées du titre.

    :param pdf_path: Chemin du fichier PDF à traiter
    :return: Texte brut nettoyé
    """
    title_to_remove = "Document Éducatif : La Deuxième Guerre Mondiale"

    # Variable pour stocker le texte extrait
    clean_text = ""

    # Ouvre le fichier PDF
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            # Extraire le texte brut de chaque page
            page_text = page.get_text()

            # Supprimer le titre de la page si présent
            page_text = page_text.replace(title_to_remove, "")

            # Ajouter le texte nettoyé à la variable principale
            clean_text += page_text

    return clean_text

# Fonction pour extraire les notions
def extract_notions_from_text(text):
    # Regex pour capturer toutes les notions (en prenant en compte les retours à la ligne)
    pattern_notions = r"(Notion \d+\.\d+\.\d+ :.*?)(?=\nNotion \d+\.\d+\.\d+ :|\Z)"

    # Trouver toutes les notions dans le texte
    resultats_notions = re.findall(pattern_notions, text, re.DOTALL)

    return resultats_notions


# Fonction pour traiter le PDF et sauvegarder dans MongoDB
def process_pdf_and_save_to_db(pdf_path):
    # Extraire le texte complet du PDF
    text_nettoye = extract_clean_text(pdf_path)

    # Extraire les notions du texte
    notions = extract_notions_from_text(text_nettoye)
    notions = "\n".join(notions)
    # Si notions est une liste extraite précédemment

    pattern = r"(Notion \d+\.\d+\.\d+ : .*?)(?=\n\s*(Notion \d+\.\d+\.\d+ :|Partie|Chapitre|$))"
    # Rechercher toutes les correspondances
    matches = re.findall(pattern, notions, re.DOTALL)

    # Extraire uniquement la première partie des correspondances et nettoyer
    notions = [match[0].replace("\n", " ").strip() for match in matches]
    # Étape 3 : Sauvegarder chaque notion dans MongoDB
    pattern_detail = r"Notion (\d+)\.(\d+)\.(\d+) : (.+)"
    for notion in notions:
        match = re.match(pattern_detail, notion)
        if match:
            notion_data = {
                "part_num": int(match.group(1)),  # Numéro de partie
                "chap_num": int(match.group(2)),  # Numéro de chapitre
                "notion_num": int(match.group(3)),  # Numéro de notion
                "contenu": match.group(4).strip()  # Contenu de la notion
            }
            save_notion_to_db(notion_data)  # Sauvegarde en base
            print(f"Notion sauvegardée : {notion_data}")
        else:
            print(f"Format invalide pour la notion : {notion}")

    print("Toutes les notions ont été sauvegardées dans MongoDB.")


pdf_path = 'C:/Users/bihay/Documents/alone/deuxieme_guerre_mondiale.pdf'

# Chemin du fichier PDF


# Traiter le PDF et sauvegarder les données dans MongoDB
process_pdf_and_save_to_db(pdf_path)
