from django.shortcuts import render

def register_view(request):

    return render(request, 'accounts/pages/register.html', {
    })
