from django.urls import path

from . import views

# Define namespace
app_name = 'adviser'

urlpatterns = [
    path('', views.index, name='index'),
    path('gpt/', views.gpt, name='gpt_base'),
    path('gpt/<str:document_id>/', views.gpt, name='gpt'),
]