from django.shortcuts import render

def PersonLinks(request):
    return render(request, 'persons/person_index.html')