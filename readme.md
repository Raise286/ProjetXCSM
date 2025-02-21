# Documentation de l'API de Parsing de Documents

## Prérequis

Avant d'utiliser cette API, assurez-vous d'avoir installé les éléments suivants :

- Python 3.x
- Django
- Django REST Framework (`djangorestframework`)
- Djongo (`djongo`)
- PyMuPDF (`pymupdf`)
- MongoDB (pour la base de données, utilisée avec Djongo)

## Installation

1. Clonez le dépôt du projet :
   ```bash
   git clone <URL_DU_REPO>
   cd <NOM_DU_PROJET>
   ```
2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv env
   source env/bin/activate  # Pour Linux/macOS
   env\Scripts\activate  # Pour Windows
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Configurez votre base de données MongoDB dans `settings.py` :
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'djongo',
           'NAME': 'nom_de_la_base',
       }
   }
   ```
5. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```
6. Lancez le serveur Django :
   ```bash
   python manage.py runserver
   ```

## Utilisation de l'API

### Endpoints disponibles

| Methode | URL                | Description |
|---------|--------------------|-------------|
| POST    | `/upload_pdf/`         | Uploader un document pour parsing |
| GET     | `/notion/<str:notion_number>/` | Obtenir une notion specifique du document a partir de son numero dans le document  |

### Exemples de requetes

#### 1. Uploader un document

Utilisez un client HTTP comme `curl` ou Postman pour envoyer un fichier PDF :
```bash
curl -X POST http://127.0.0.1:8000/upload_pdf/ \
     -F "file=@chemin_vers_fichier.pdf"
```



#### 2. Obtenir une notion specifique a partir de son numero dans le document 
```bash
curl -X GET http://127.0.0.1:8000/notion/<id>/
```

## Fonctionnalités
- Extraction automatique du texte des fichiers PDF
- segmentation du document en notion 
- Stockage des documents et de leur contenu dans MongoDB
- obtention d'une notion specifique du document 

## Ameliorations futures
- Support d'autres formats de documents (DOCX, TXT, etc.)
- Authentification et permissions
- Interface frontend pour visualiser les documents

## Auteur
Nom : Bihay Raphael   
Email : Raphaelbihay286@gmail.com  

---

Ce README fournit une base claire pour comprendre, installer et utiliser  l'API Django de parsing de documents.

