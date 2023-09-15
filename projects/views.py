from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.models import Project, Post, Comment
from projects.forms import ProjectForm, PostForm, CommentForm
from django.urls import reverse
from accounts.models import CustomUser
from django.http import Http404

@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ProjectDashboard(View):

    def render_template(self, form, project_pk):
        return render(
            self.request,
            'projects/pages/project_dashboard.html',
            context={
                'form': form,
                'project_pk': project_pk,
            }
        )
    
    def get_project(self, project_pk=None):
        project = None

        if project_pk is not None:
            project = get_object_or_404(Project, composite_pk=project_pk)

        return project

    def get(self, request, project_pk=None):

        project = self.get_project(project_pk)
        form = ProjectForm(instance=project)

        return self.render_template(form, project_pk)

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

            messages.success(request, 'O projeto foi criado com sucesso!')
            return redirect (reverse('projects:project_detail', args=[project.composite_pk]))

        messages.error(request, 'Há campos incorretos no formulário')
        return self.render_template(form)


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
                'mods': self.get_mods(project)
            })
    
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
        comments = self.get_comments(post)
        comment_form = CommentForm()
        project = get_object_or_404(Project, composite_pk=post.project.composite_pk)
        return render(self.request, 'projects/pages/post_detail.html',
            context={
                'comments': comments,
                'post': post,
                'user': user,
                'project': project,
                'comment_form': comment_form,
            })
    
    def get_comments(self, post):
        return Comment.objects.filter(post=post).order_by("created")
    
    def get(self, request, post_pk):
        post = Post.objects.get(composite_pk=post_pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        if not post.project.members.filter(pk=user.pk).exists() and not post.project.owner == user:
            raise Http404
        
        user = CustomUser.objects.get(pk=request.user.pk)
        return self.render_template(user, post)
    

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

    def render_template(self, projects):
        return render(
            self.request,
            'projects/pages/projects.html',
            context={
                'projects_page': True,
                'projects': projects,
            }
        )
    
    def get_projects(self):
        return Project.objects.all()

    def get(self, request):

        projects = self.get_projects()

        return self.render_template(projects)
    
def enter_project(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    project = Project.objects.get(composite_pk=project_pk)
    user = CustomUser.objects.get(pk=request.user.pk)

    project.members.add(user)
    project.save()

    return redirect (reverse('projects:project_detail', args=[project_pk]))

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
            })
    
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
    
def delete_project(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    project = Project.objects.get(composite_pk=project_pk)
    user = CustomUser.objects.get(pk=request.user.pk)

    if not project.owner == user:
        messages.error(request, 'Você não tem permissão para excluir este Projeto.')
        return redirect (reverse('projects:project_detail', args=[project_pk]))
    
    project.delete()
    messages.success(request, 'O projeto foi excluído com sucesso')
    return redirect (reverse('projects:projects'))

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

    messages.success(request, 'O usuário agora é um moderador')
    return redirect (reverse('projects:members_list', args=[project_pk]))

def remove_mod(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)
    
    project.mods.remove(user)
    project.save()

    messages.success(request, 'O usuário não é mais moderador')
    return redirect (reverse('projects:members_list', args=[project_pk]))

def remove_member(request):
    if not request.POST:
        raise Http404
    
    project_pk = request.POST.get('project_composite_pk')
    user = CustomUser.objects.get(cpf=request.POST.get('user'))
    project = Project.objects.get(composite_pk=project_pk)

    
    project.members.remove(user)
    project.save()

    messages.success(request, 'O membro foi removido')
    return redirect (reverse('projects:members_list', args=[project_pk]))

def delete_post(request):
    if not request.POST:
        raise Http404
    
    post_pk = request.POST.get('post_composite_pk')
    post = Post.objects.get(composite_pk=post_pk)
    project_pk = post.project.composite_pk
    
    post.delete()
    messages.success(request, 'O post foi deletado')
    return redirect (reverse('projects:project_detail', args=[project_pk]))
