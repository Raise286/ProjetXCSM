from django.urls import path
from .views import UploadPDFView
from .views import HomeApiView
from .views import NotionDetailApiView

urlpatterns = [
    path('',HomeApiView.as_view(),name='home'),
    path('upload_pdf/', UploadPDFView.as_view(), name='upload_pdf'),
    path('notion/<str:notion_number>/',NotionDetailApiView.as_view(),name='notion_detail')
]
