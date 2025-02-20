from rest_framework import serializers

class NotionSerializer(serializers.Serializer):
    part_num = serializers.IntegerField()
    chap_num = serializers.IntegerField()
    notion_num = serializers.IntegerField()
    contenu = serializers.CharField()
