from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DocumentForm
from .models import Document

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
