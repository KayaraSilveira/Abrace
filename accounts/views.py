from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm, EditProfileForm, ProfileCategoriesForm, ReviewForm
from django.contrib.auth.models import User
from django.http import Http404
from .models import CustomUser, Category, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from projects.models import Project
from django.db.models import Q
from django.shortcuts import get_object_or_404

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
                return redirect(reverse('projects:projects'))

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

@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class ProfileEdit(View):

    def render_template(self, form, categories):
        return render(
            self.request,
            'accounts/pages/edit_profile.html',
            context={
                'form': form,
                'form_categories': categories,
                'profile_page': True,
                'profile_tab': True,
            }
        )

    def get(self, request):

        profile = CustomUser.objects.get(pk=request.user.pk)
        form = EditProfileForm(instance=profile)
        categories = ProfileCategoriesForm(instance=profile)

        return self.render_template(form, categories)

    def post(self, request):

        profile = CustomUser.objects.get(pk=request.user.pk)

        form = EditProfileForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=profile, 
        )

        if form.is_valid():

            form.save()

            messages.success(request, 'O perfil foi alterado com sucesso!')
            return redirect(reverse('accounts:profile'))

        categories = ProfileCategoriesForm(instance=profile)
        messages.error(request, 'Há campos incorretos no formulário')
        return self.render_template(form, categories)

@login_required(login_url='accounts:login', redirect_field_name='next')
def save_categories(request):
    if not request.POST:
        raise Http404

    profile = CustomUser.objects.get(pk=request.user.pk)

    form = ProfileCategoriesForm(
            data=request.POST or None,
            instance=profile, 
    )

    if form.is_valid():
        form.save()
    else:
        profile.categories.set('')
        profile.save()

    messages.success(request, 'As preferências foram alteradas com sucesso!')
    return redirect(reverse('accounts:profile'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class MyProjectsList(View):

    def render_template(self, projects, profile, role):
        return render(
            self.request,
            'accounts/pages/my_projects.html',
            context={
                'projects': projects,
                'profile_page': True,
                'project_tab': True,
                'profile': profile,
                'role': role,
            }
        )

    def get(self, request, role=None):

        profile = CustomUser.objects.get(pk=request.user.pk)

        if role:
            if role == 'Dono':
                projects = Project.objects.filter(owner=profile)
            elif role == 'Moderador':
                projects = Project.objects.filter(mods=profile)
            else:
                projects = Project.objects.filter(members=profile)
        else:
            projects_owner = Project.objects.filter(owner=profile)
            projects_members = Project.objects.filter(members=profile)
            projects = projects_owner.union(projects_members)

        return self.render_template(projects, profile, role)

@login_required(login_url='accounts:login', redirect_field_name='next')
def review_view(request):
    profile = get_object_or_404(CustomUser, pk=request.user.pk)
    reviews = Review.objects.filter(reviewed_user=profile)

    return render(request, 'accounts/pages/reviews.html', {
        'profile': profile,
        'reviews': reviews,
        'profile_page': True,
        'review_tab': True,
    })
    
@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class ReviewCreateView(View):

    def render_template(self, form, reviewed_user, project, author_user):
        return render(self.request, 'accounts/pages/review_create.html', {
            'form': form,
            'reviewed_user': reviewed_user,
            'project': project,
            'user': author_user
        })

    def get(self, request, reviewed_pk, project_pk):

        author_user = CustomUser.objects.get(pk=request.user.pk)
        reviewed_user = CustomUser.objects.get(pk=reviewed_pk)
        project = Project.objects.get(composite_pk=project_pk)
        form = ReviewForm()

        return self.render_template(form, reviewed_user, project, author_user)

    def post(self, request, reviewed_pk, project_pk):

        form = ReviewForm(request.POST)
        project_pk = request.POST.get('project_composite_pk')
        project = Project.objects.get(composite_pk=project_pk)

        review = form.save(commit=False)

        author_user = CustomUser.objects.get(pk=request.user.pk)
        reviewed_user = CustomUser.objects.get(cpf=request.POST.get('reviewed_user_cpf'))

        review.author_user = author_user
        review.reviewed_user = reviewed_user
        review.project = project

        auto_id = Review.objects.filter(reviewed_user=reviewed_user, project=project)

        if auto_id:
            review.review_id = auto_id.last().review_id + 1
        else:
            review.review_id = 0

        review.save()

        messages.success(request, 'Sua avaliação foi enviada.')
        return redirect (reverse('projects:members_list', args=[project_pk]))

@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ViewProfile(View):

    def render_template(self, profile, categories):
        return render(
            self.request,
            'accounts/pages/view_profile.html',
            context={
                'profile': profile,
                'profile_tab': True,
                'categories': categories,
            }
        )

    def get(self, request, cpf):
        profile = CustomUser.objects.get(cpf=cpf)
        categories = Category.objects.all()
        return self.render_template(profile, categories)
    
@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ViewProfileProjects(View):

    def render_template(self, projects, profile, role):
        return render(
            self.request,
            'accounts/pages/view_profile_projects.html',
            context={
                'projects': projects,
                'project_tab': True,
                'profile': profile,
                'role': role,
            }
        )

    def get(self, request, cpf, role=None):

        profile = CustomUser.objects.get(cpf=cpf)

        if role:
            if role == 'Dono':
                projects = Project.objects.filter(owner=profile)
            elif role == 'Moderador':
                projects = Project.objects.filter(mods=profile)
            else:
                projects = Project.objects.filter(members=profile)
        else:
            projects_owner = Project.objects.filter(owner=profile)
            projects_members = Project.objects.filter(members=profile)
            projects = projects_owner.union(projects_members)

        return self.render_template(projects, profile, role)

@login_required(login_url='accounts:login', redirect_field_name='next')
def view_profile_review(request, cpf):
    profile = get_object_or_404(CustomUser, cpf=cpf)
    reviews = Review.objects.filter(reviewed_user=profile)
    user = CustomUser.objects.get(pk=request.user.pk)

    return render(request, 'accounts/pages/view_reviews.html', {
        'profile': profile,
        'reviews': reviews,
        'review_tab': True,
        'user': user,
    })