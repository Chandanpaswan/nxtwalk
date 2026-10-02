from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import CaseStudy


def case_study_list(request):
    studies = CaseStudy.objects.filter(
        is_published=True,
        project__is_published=True,
    ).select_related("project")
    page_obj = Paginator(studies, 6).get_page(request.GET.get("page"))
    return render(request, "case_studies/list.html", {"case_studies": page_obj.object_list, "page_obj": page_obj})


def case_study_detail(request, slug):
    study = get_object_or_404(
        CaseStudy.objects.select_related("project").filter(
            is_published=True,
            project__is_published=True,
        ),
        project__slug=slug,
    )
    return render(request, "case_studies/detail.html", {"study": study})