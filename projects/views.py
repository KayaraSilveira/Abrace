from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.models import Project
from projects.forms import ProjectForm
from django.urls import reverse
from accounts.models import CustomUser

@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ProjectDashboard(View):

    def render_template(self, form):
        return render(
            self.request,
            'projects/pages/project_dashboard.html',
            context={
                'form': form,
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

        return self.render_template(form)

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
                    project.project_id = auto_id.last() + 1
                else:
                    project.project_id = 0

            project.save()

            messages.success(request, 'O projeto foi criado com sucesso!')
            return redirect(reverse('accounts:profile'))

        messages.error(request, 'Há campos incorretos no formulário')
        return self.render_template(form)


