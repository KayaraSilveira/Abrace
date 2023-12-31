from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.models import Project, Post, Comment
from projects.forms import ProjectForm, PostForm, CommentForm, ProjectCategoriesForm
from django.urls import reverse
from accounts.models import CustomUser, Category
from django.http import Http404
from django.db.models import Q

@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ProjectDashboard(View):

    def render_template(self, form, project_pk, form_categories, project_active=False, project_img=False):
        return render(
            self.request,
            'projects/pages/project_dashboard.html',
            context={
                'form': form,
                'project_pk': project_pk,
                'form_categories': form_categories,
                'project_active': project_active,
                'project_img': project_img,
                'return_page': self.get_return_page(),
            }
        )
    
    def get_return_page(self):
        next_param = self.request.GET.get('next', None)
        if not next_param:
            next_param = "/"
        return next_param
    
    def get_project(self, project_pk=None):
        project = None

        if project_pk is not None:
            project = get_object_or_404(Project, composite_pk=project_pk)

        return project

    def get(self, request, project_pk=None):

        project = self.get_project(project_pk)
        form = ProjectForm(instance=project)
        form_categories = None
        project_active = False
        project_img = False

        if project_pk:
            form_categories = ProjectCategoriesForm(instance=project)
            project_active = project.status
            project_img = project.cover_photo

        return self.render_template(form, project_pk, form_categories, project_active, project_img)

    def post(self, request, project_pk=None):

        project = self.get_project(project_pk)

        form = ProjectForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=project, 
        )

        if form.is_valid():

            project = form.save(commit=False)
            owner = CustomUser.objects.get(pk=request.user.pk)
            project.owner = owner

            if not project_pk:
                auto_id = Project.objects.filter(owner=owner)

                if auto_id:
                    project.project_id = auto_id.last().project_id + 1
                else:
                    project.project_id = 0

            project.save()
            
            if project_pk:
                messages.success(request, 'O projeto foi salvo com sucesso!')
                return redirect (reverse('projects:project_detail', args=[project.composite_pk]))
            return redirect (reverse('projects:set_categories', args=[project.composite_pk]))

        project_active = False
        form_categories = None
        project_img = False
        if project_pk:
            form_categories = ProjectCategoriesForm(instance=project)
            project_active = project.status
            project_img = project.cover_photo

        messages.error(request, 'Há campos incorretos no formulário')
        return self.render_template(form, project_pk, form_categories, project_active, project_img)


@login_required(login_url='accounts:login', redirect_field_name='next')    
def save_categories(request, project_pk):
    if not request.POST:
        raise Http404
    
    project = get_object_or_404(Project, composite_pk=project_pk)

    form = ProjectCategoriesForm(data=request.POST or None, instance=project)

    if form.is_valid():
        form.save()
    else:
        project.categories.set('')
        project.save()


    messages.success(request, 'As categorias foram alteradas com sucesso!')
    return redirect (reverse('projects:project_detail', args=[project_pk]))

def set_categories(request, project_pk):
    project = get_object_or_404(Project, composite_pk=project_pk)
    form_categories = ProjectCategoriesForm(instance=project)
    return render(request,
            'projects/pages/project_categories.html',
            context={
                'form_categories': form_categories,
                'project_pk': project_pk,
            }
        )


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class ProjectDetail(View):

    def render_template(self, user, project):
        return render(self.request, 'projects/pages/project_detail.html',
            context={
                'is_member': self.is_member(user, project),
                'project': project,
                'posts': self.get_posts(project),
                'user': user,
                'post_form': PostForm(),
                'members': self.get_members(project),
                'mods': self.get_mods(project),
                'solicitation': self.get_solicitation(project),
                'return_page': self.get_return_page(),
            })
    
    def get_return_page(self):
        next_param = self.request.GET.get('next', None)
        if not next_param:
            next_param = "/"
        return next_param
    
    def get_solicitation(self, project):
        return project.solicitation.all()

    def get_mods(self, project):
        return project.mods.all()
    
    def get_project(self, project_pk):
        project = get_object_or_404(Project, composite_pk=project_pk)
        return project
    
    def is_member(self, user, project):
        return project.members.filter(pk=user.pk).exists() or project.owner == user
    
    def get_members(self, project):
        return project.members.all()[:3]
    
    def get_posts(self, project):
        return Post.objects.filter(project=project).order_by("-created")
    
    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        return self.render_template(user, project)


@login_required(login_url='accounts:login', redirect_field_name='next')
def send_post(request):
    if not request.POST:
        raise Http404

    form = PostForm(request.POST)
    project_pk = request.POST.get('project_composite_pk')
    project = Project.objects.get(composite_pk=project_pk)


    post = form.save(commit=False)
    
    autor = CustomUser.objects.get(pk=request.user.pk)
    post.autor = autor
    post.project = project

    auto_id = Post.objects.filter(autor=autor, project=project)

    if auto_id:
        post.post_id = auto_id.last().post_id + 1
    else:
        post.post_id = 0

    post.save()

    messages.success(request, 'Sua postagem foi enviada.')
    return redirect (reverse('projects:project_detail', args=[project_pk]))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class PostDetail(View):

    def render_template(self, user, post):
        project = get_object_or_404(Project, composite_pk=post.project.composite_pk)
        return render(self.request, 'projects/pages/post_detail.html',
            context={
                'comments': self.get_comments(post),
                'post': post,
                'user': user,
                'project': project,
                'comment_form': CommentForm(),
                'mods': self.get_mods(project),
                'return_page': self.get_return_page(),
            })
    
    def get_return_page(self):
        next_param = self.request.GET.get('next', None)
        if not next_param:
            next_param = "/"
        return next_param
    
    def get_mods(self, project):
        return project.mods.all()
    
    def get_comments(self, post):
        return Comment.objects.filter(post=post).order_by("created")
    
    def get(self, request, post_pk):
        post = Post.objects.get(composite_pk=post_pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        if not post.project.members.filter(pk=user.pk).exists() and not post.project.owner == user:
            raise Http404
        
        user = CustomUser.objects.get(pk=request.user.pk)
        return self.render_template(user, post)


@login_required(login_url='accounts:login', redirect_field_name='next')
def send_comment(request):
    if not request.POST:
        raise Http404

    form = CommentForm(request.POST)
    post_pk = request.POST.get('post_composite_pk')
    post = Post.objects.get(composite_pk=post_pk)


    comment = form.save(commit=False)
    
    autor = CustomUser.objects.get(pk=request.user.pk)
    comment.autor = autor
    comment.post = post

    auto_id = Comment.objects.filter(autor=autor, post=post)

    if auto_id:
        comment.comment_id = auto_id.last().comment_id + 1
    else:
        comment.comment_id = 0

    comment.save()

    messages.success(request, 'Seu Comentário foi enviado.')
    return redirect (reverse('projects:post_detail', args=[post_pk]))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class ProjectsList(View):

    def render_template(self, projects, category_active, recommendations):
        user = CustomUser.objects.get(pk=self.request.user.pk)
        categories = Category.objects.all()
        return render(
            self.request,
            'projects/pages/projects.html',
            context={
                'projects_page': True,
                'projects': projects,
                'user': user,
                'categories': categories,
                'category_active': category_active,
                'recommendations': recommendations,
            }
        )
    
    def get_recommendations(self):
        user = CustomUser.objects.get(pk=self.request.user.pk)
        recommendations = []
        user_categories = user.categories.all()

        if not user_categories:
            recommendations = Project.objects.all()[:3]

        else:
            for category in user_categories:
                project = Project.objects.exclude(composite_pk__in=[p.composite_pk for p in recommendations]).exclude(owner=user).exclude(members=user).exclude(status=False).filter(categories=category).first()

                if project:
                    recommendations.append(project)

                if len(recommendations) >= 3:
                    break

            if len(recommendations) < 3:
                remaining_projects = Project.objects.exclude(composite_pk__in=[p.composite_pk for p in recommendations]).exclude(owner=user).exclude(members=user).exclude(status=False)[:3 - len(recommendations)]
                recommendations.extend(remaining_projects)

        return recommendations

    def get(self, request, category=None):

        category_active = None
        recommendations = None

        if category:
            category_active = Category.objects.get(title=category)
            projects = Project.objects.filter(categories=category_active, status=True)
            
        else:
            projects = Project.objects.filter(status=True)
            recommendations = self.get_recommendations


        return self.render_template(projects, category_active, recommendations)
    

@login_required(login_url='accounts:login', redirect_field_name='next')
def leave_project(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    project = Project.objects.get(composite_pk=project_pk)
    user = CustomUser.objects.get(pk=request.user.pk)

    project.members.remove(user)
    project.save()

    return redirect (reverse('projects:project_detail', args=[project_pk]))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class MembersList(View):

    def render_template(self, user, project):
        return render(self.request, 'projects/pages/members.html',
            context={
                'is_member': self.is_member(user, project),
                'is_mod': self.is_mod(user, project),
                'is_owner': self.is_owner(user, project),
                'project': project,
                'user': user,
                'members': self.get_members(project),
                'mods': self.get_mods(project),
                'return_page': self.get_return_page(),
            })
    
    def get_return_page(self):
        next_param = self.request.GET.get('next', None)
        if not next_param:
            next_param = "/"
        return next_param
    
    def get_project(self, project_pk):
        project = get_object_or_404(Project, composite_pk=project_pk)
        return project
    
    def is_member(self, user, project):
        return project.members.filter(pk=user.pk).exists() or project.owner == user
    
    def is_owner(self, user, project):
        return project.owner == user

    def is_mod(self, user, project):
        return project.mods.filter(pk=user.pk).exists() or project.owner == user
    
    def get_members(self, project):
        return project.members.all()
    
    def get_mods(self, project):
        return project.mods.all()
    
    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        return self.render_template(user, project)


@login_required(login_url='accounts:login', redirect_field_name='next')   
def delete_project(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    project = Project.objects.get(composite_pk=project_pk)
    password = request.POST.get('password')
    user = CustomUser.objects.get(pk=request.user.pk)

    if not project.owner == user:
        messages.error(request, 'Você não tem permissão para excluir este Projeto.')
        return redirect (reverse('projects:project_detail', args=[project_pk]))
    
    if user.check_password(password):
        project.delete()
        messages.success(request, 'O projeto foi excluído com sucesso')
        return redirect (reverse('projects:projects'))
    
    else:
        messages.error(request, 'Senha incorreta. O projeto não foi excluído.')
        return redirect (reverse('projects:project_edit', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def add_mod(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)

    if not project.owner == CustomUser.objects.get(pk=request.user.pk):
        raise Http404
    
    project.mods.add(user)
    project.save()

    return redirect (reverse('projects:members_list', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def remove_mod(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)
    
    project.mods.remove(user)
    project.save()

    return redirect (reverse('projects:members_list', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def remove_member(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)
    
    project.members.remove(user)
    project.save()

    return redirect (reverse('projects:members_list', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def delete_post(request):
    if not request.POST:
        raise Http404
    
    post_pk = request.POST.get('post_composite_pk')
    post = Post.objects.get(composite_pk=post_pk)
    project_pk = post.project.composite_pk
    
    post.delete()
    return redirect (reverse('projects:project_detail', args=[project_pk]))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
) 
class Solicitation(View):

    def render_template(self, project):
        return render(self.request, 'projects/pages/solicitation.html',
            context={
                'project': project,
                'solicitation': self.get_solicitation(project),
                'return_page': self.get_return_page(),
            })
    
    def get_return_page(self):
        next_param = self.request.GET.get('next', None)
        if not next_param:
            next_param = "/"
        return next_param
    
    def get_project(self, project_pk):
        project = get_object_or_404(Project, composite_pk=project_pk)
        return project
    
    def get_solicitation(self, project):
        return project.solicitation.all()
    
    
    def get(self, request, project_pk):

        user = CustomUser.objects.get(pk=request.user.pk)
        project = self.get_project(project_pk)

        if not user == project.owner and user not in project.mods.all():
            raise Http404
        
        return self.render_template(project)


@login_required(login_url='accounts:login', redirect_field_name='next')   
def add_solicitation(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(composite_pk=project_pk)
    
    project.solicitation.add(user)
    project.save()

    return redirect (reverse('projects:project_detail', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def remove_solicitation(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(composite_pk=project_pk)
    
    project.solicitation.remove(user)
    project.save()

    return redirect (reverse('projects:project_detail', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def accept_solicitation(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)
    
    project.solicitation.remove(user)
    project.members.add(user)
    project.save()

    return redirect (reverse('projects:project_solicitation', args=[project_pk]))


@login_required(login_url='accounts:login', redirect_field_name='next')
def reject_solicitation(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)
    
    project.solicitation.remove(user)
    project.save()

    return redirect (reverse('projects:project_solicitation', args=[project_pk]))

@login_required(login_url='accounts:login', redirect_field_name='next')
def deactivate(request, project_pk):

    owner = CustomUser.objects.get(pk=request.user.pk)
    project = get_object_or_404(Project, composite_pk=project_pk)

    if not project.owner == owner:
        raise Http404
        
    project.status = not project.status 
    project.save()

    messages.success(request, 'As informações foram salvas')
    return redirect(reverse('projects:project_detail', args=[project_pk]))

@login_required(login_url='accounts:login', redirect_field_name='next')
def home(request):
    return render (request,'projects/pages/home.html')

@login_required(login_url='accounts:login', redirect_field_name='next')
def search_project(request):
    query = request.GET.get('query', '')
    user = CustomUser.objects.get(pk=request.user.pk)
    
    projects = Project.objects.filter(
        Q(name__icontains=query) | Q(categories__title__icontains=query) | Q(description__icontains=query),
        status=True
        ).distinct()
    
    return render(
        request,
        'projects/pages/projects_search.html',
        context={
            'projects': projects,
            'user': user,
        }
    )
