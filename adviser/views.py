from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
import os
from . import constants
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('adviser:index')
    elif request.method == 'GET':
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'adviser/index.html', {
        'form': form,
        'documents': documents,
    })

def gpt(request, document_id):
    if request.method == 'POST':
        firstQuestion = request.POST.get('firstQuestion')
        question = request.POST.get('question')
        # Get the data file with the document id
        data_file = get_object_or_404(Document, pk=document_id)
        # Get the file path
        file_path = str(settings.MEDIA_ROOT / data_file.uploaded_file.name)
        # Set the API key
        os.environ["OPENAI_API_KEY"] = constants.APIKEY
        
        # GPT API
        loader = TextLoader(file_path)
        # You can load in it an entire directory
        # loader = DirectoryLoader(".", glob="*.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])        

        if firstQuestion == "True":
            query = "Please write File ready! I am ready for the questions."
        elif firstQuestion == "False":
            query = question
            
        answer = index.query(query, llm=ChatOpenAI())
        messages.success(request, answer)

        return render(request, "adviser/gpt.html", {"data_file": data_file, "firstQuestion": "False"})

    elif request.method == 'GET':
        return redirect('index')