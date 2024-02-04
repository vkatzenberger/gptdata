from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
# import os, sys
# from . import constants
# from langchain_community.document_loaders import TextLoader
# from langchain.indexes import VectorstoreIndexCreator

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('index')
    elif request.method == 'GET':
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'adviser/index.html', {
        'form': form,
        'documents': documents,
    })

def gpt(request, document_id):
    if request.method == 'POST':
        # OpenAI API
        # os.environ["OPENAI_API_KEY"] = constants.APIKEY
        # query = "Tell me more about my file"
        # file_path = os.path.join(settings.MEDIA_ROOT, 'documents/file_001.txt')
        # loader = TextLoader(file_path)
        # index = VectorstoreIndexCreator().from_loaders([loader])
        # answer = index.query(query)
        data_file = get_object_or_404(Document, pk=document_id)
        return render(request, "adviser/gpt.html", {"data_file": data_file})

    elif request.method == 'GET':
        return redirect('index')