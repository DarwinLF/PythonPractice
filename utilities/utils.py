from django.urls import resolve

def get_breadcrumbs(request):
    breadcrumbs = []
    
    # Add the homepage as the first breadcrumb
    breadcrumbs.append({'name': 'Home', 'url': '/'})
    
    url_path = request.path
    url_parts = url_path.split('/')
    current_url = ''

    for part in url_parts:
        if part:
            current_url += '/' + part
            breadcrumbs.append({'name': part.capitalize(), 
                                'url': current_url})

    return breadcrumbs