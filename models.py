from django.db import models

class Notion(models.Model):
    part_num = models.IntegerField()
    chap_num = models.IntegerField()
    notion_num = models.IntegerField()
    contenu = models.TextField()
