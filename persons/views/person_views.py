from django.shortcuts import render

def PersonLinks(request):
    links = [
        {'url': 'author/', 'text': 'Author'},
        {'url': 'customer/', 'text': 'Customer'},
        {'url': 'employee/', 'text': 'Employee'},
    ]

    context = {'links': links}

    return render(request, 'persons/person_links.html', context)