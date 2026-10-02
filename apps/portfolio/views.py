from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Project


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    page_obj = Paginator(projects, 9).get_page(request.GET.get("page"))
    return render(request, "portfolio/list.html", {"projects": page_obj.object_list, "page_obj": page_obj})


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.filter(is_published=True).prefetch_related("gallery"),
        slug=slug,
    )
    return render(request, "portfolio/detail.html", {"project": project})