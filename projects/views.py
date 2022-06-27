from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.test import tag
from .models import Project, Review
from .forms import ProjectForm, ReviewForm
from .utils import search_project, paginate_project
from django.contrib import messages


# Create your views here.
def projects(request):
    projects, search_query = search_project(request)
    custom_range, projects = paginate_project(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.get_vote_count()
        messages.success(request, 'Comment was added successfully')
        return redirect('project', pk)
    context = {
        'project': projectObj,
        'form': form,
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = project.tags.get_or_create(name=tag)

            return redirect('projects')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = project.tags.get_or_create(name=tag)
                # project.tags.add(tag)
            return redirect('projects')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, "projects/delete_template.html", context)
