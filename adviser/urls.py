from django.urls import path

from . import views

# Define namespace
app_name = 'adviser'

urlpatterns = [
    path('', views.index, name='index'),
    path('gpt/', views.gpt, name='gpt_base'),
    path('gpt/<int:document_id>/', views.gpt, name='gpt'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
]