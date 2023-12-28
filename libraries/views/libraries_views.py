from django.shortcuts import render

def LibrariesLinks(request):
    return render(request, 'libraries/libraries_index.html')