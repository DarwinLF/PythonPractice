from django.shortcuts import render

def main(request):
    links = [
        {'url': 'polls/', 'text': 'Polls'},
        {'url': 'persons/', 'text': 'Persons'},
        {'url': 'libraries/', 'text': 'Libraries'},
    ]

    context = {'links': links}

    return render(request, 'main/home.html', context)