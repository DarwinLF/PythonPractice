from django.shortcuts import render

def LibrariesLinks(request):
    links = [
        {'url': 'library/', 'text': 'Library'},
        {'url': 'book/', 'text': 'Book'},
        {'url': 'rent/', 'text': 'Rent'},
    ]

    context = {'links': links}

    return render(request, 'libraries/libraries_links.html', context)