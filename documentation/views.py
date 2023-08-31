from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def documentation(request):
    return render(request, 'documentation/pages/documentation_list.html')

@user_passes_test(lambda u: u.is_superuser)
def documentation_routes(request):
    return render(request, 'documentation/pages/routes.html')