from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os
import pymongo

from .serializers import NotionSerializer
from .utils import process_pdf_and_save_to_db  # Ta fonction de traitement du PDF
from .utils import save_notion_to_db
from .utils import extract_clean_text
from .utils import extract_notions_from_text
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient


# Fonction pour se connecter à MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Documents"]
    return db["notions"]  # Collection des notions


class NotionDetailApiView(APIView):
    def get(self, request, notion_number, format=None):
        # Connexion à la base de données MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Documents"]
        collection = db["notions"]

        # Diviser le notion_number (par exemple "3.2.2") en trois parties
        try:
            part_num, chap_num, notion_num = map(int, notion_number.split('.'))
        except ValueError:
            return Response({"error": "Invalid format. Use part.chap.notion (e.g., 3.2.2)"}, status=status.HTTP_400_BAD_REQUEST)

        # Rechercher la notion dans la collection en utilisant part_num, chap_num, et notion_num
        notion = collection.find_one({
            "part_num": part_num,
            "chap_num": chap_num,
            "notion_num": notion_num
        })

        if notion:
            # Si la notion est trouvée, renvoyer les données
            return Response(notion, status=status.HTTP_200_OK)
        else:
            # Si la notion n'existe pas, renvoyer une erreur 404
            return Response({"error": "Notion not found"}, status=status.HTTP_404_NOT_FOUND)

class UploadPDFView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Vérifier si le fichier a bien été transmis
        file = request.FILES.get('pdf_file')
        if not file:
            return Response({"error": "No PDF file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarder le fichier dans un dossier temporaire
        pdf_path = os.path.join("temp", file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Appeler la fonction pour traiter le PDF et sauvegarder les données
        try:
            process_pdf_and_save_to_db(pdf_path)
            return Response({"message": "Notions saved successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERRO)
class HomeApiView(APIView):
    def get(self,request,format=None):
        dat={
            "Bienvenue sur le site de parsage des documents "
        }
        return Response(dat)