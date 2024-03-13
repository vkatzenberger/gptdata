from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
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
        firstQuestion = bool(request.POST.get('firstQuestion'))
        
        loadAll = bool(request.POST.get('loadAll'))
        question = request.POST.get('question')
        data_file = get_object_or_404(Document, pk=document_id)
        

        if loadAll == False:
            file_path = str(settings.MEDIA_ROOT / data_file.uploaded_file.name)
            loader = TextLoader(file_path)
        else:
            file_path = str(settings.MEDIA_ROOT) + "\\documents\\"
            loader = DirectoryLoader(file_path, glob="*.txt", loader_cls=TextLoader)
        
        # Set the API key
        os.environ["OPENAI_API_KEY"] = constants.APIKEY
        
        
        index = VectorstoreIndexCreator().from_loaders([loader])       
        
        if firstQuestion == True:
            query = "Please write I am ready for the questions!"
        else:
            query = question
           
        answer = index.query(query, llm=ChatOpenAI(model="gpt-3.5-turbo-0125"))
        messages.success(request, answer)

        return render(request, "adviser/gpt.html", {"data_file": data_file if not loadAll else None, "firstQuestion": "", "loadAll" : "" if not loadAll else loadAll})
        

    elif request.method == 'GET':
        return redirect('index')
    
@require_http_methods(['DELETE'])
def delete_document(request, document_id):
    # Get the data file with the document id
    data_file = get_object_or_404(Document, pk=document_id)
    # Get the file path
    file_path = str(settings.MEDIA_ROOT / data_file.uploaded_file.name)
    # Delete the file
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the document object
    data_file.delete()
    return JsonResponse({'message': 'Document deleted successfully'}, status=204)