from django.shortcuts import render, get_object_or_404
from .models import Document
from django.http import FileResponse

# Create your views here.
def main(request):
    return render(request, 'pages/main.html')

def about_us(request):
    return render(request, 'pages/about_us.html')

def contact(request):
    return render(request, 'pages/contact.html')

def documents(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    response = FileResponse(document.pdf.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
    return response