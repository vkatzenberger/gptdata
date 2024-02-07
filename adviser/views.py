from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
import os
from . import constants
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

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
        # Get the data file with the document id
        data_file = get_object_or_404(Document, pk=document_id)
        messages.success(request, 'File passed successfully!')
        # Set the API key
        os.environ["OPENAI_API_KEY"] = constants.APIKEY
        # Add a question to query
        query = "How old are the chinchillas?"
        file_path = str(settings.MEDIA_ROOT / data_file.uploaded_file.name)
        # Test before working with GPT
        print(f"Query: {query}")
        print(f"File path: {file_path}")
        # GPT API
        loader = TextLoader(file_path)
        index = VectorstoreIndexCreator().from_loaders([loader])
        answer = index.query(query)
        
        # Print the answer
        print(f"Answer: {answer}")

        return render(request, "adviser/gpt.html", {"data_file": data_file})

    elif request.method == 'GET':
        return redirect('index')