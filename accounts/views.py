from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import Http404
from .models import CustomUser, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View

@login_required(login_url='accounts:login', redirect_field_name='next')
def profile(request):

    return render(request, 'accounts/pages/profile.html', {
    })

def register_view(request):

    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)

    return render(request, 'accounts/pages/register.html', {
        'form': form,
    })

def register_create(request):

    if not request.POST:
        raise Http404

    POST = request.POST

    request.session['register_form_data'] = POST

    form = RegisterForm(POST, request.FILES)

    if form.is_valid():

        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        del (request.session['register_form_data'])
        messages.success(request, 'A conta foi criada com sucesso')

        authenticated_user = authenticate(
            username=user.email,
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
        
            return redirect(reverse('accounts:profile'))
    
    messages.error(request, 'Erro ao criar conta')

    return redirect('accounts:register')

def login_view(request):

    login_form_data = request.session.get('login_form_data')
    form = LoginForm(login_form_data)

    return render(request, 'accounts/pages/login.html', {
        'form': form,
    })

def login_create(request):

    if not request.POST:
        raise Http404

    POST = request.POST

    request.session['login_form_data'] = POST

    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('email', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            if request.session.get('login_form_data') is not None:
                del (request.session['login_form_data'])
                return redirect(reverse('accounts:profile'))

        else:
            messages.error(request, 'Senha ou usuário inválido')

    return redirect(reverse('accounts:login'))

@login_required(login_url='accounts:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return Http404

    logout(request)
    return redirect(reverse('accounts:login'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ProfileDetail(View):

    def render_template(self, profile, categories):
        return render(
            self.request,
            'accounts/pages/profile.html',
            context={
                'profile': profile,
                'profile_page': True,
                'profile_tab': True,
                'categories': categories,
            }
        )

    def get(self, request):

        profile = CustomUser.objects.get(pk=request.user.pk)
        categories = Category.objects.all()

        return self.render_template(profile, categories)

    