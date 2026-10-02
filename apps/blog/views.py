from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Category, Post, Tag


def _published_posts():
    return Post.objects.filter(
        status=Post.PUBLISHED,
        published_at__lte=timezone.now(),
    ).select_related("author", "category").prefetch_related("tags")

def post_list(request):
    posts = _published_posts()
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
    category_slug = request.GET.get("category", "").strip()
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
        "query": query,
        "categories": Category.objects.all(),
    })


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = _published_posts().filter(category=category)
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
        "categories": Category.objects.all(),
        "active_category": category,
    })


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = _published_posts().filter(tags=tag)
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
        "categories": Category.objects.all(),
        "active_tag": tag,
    })

def post_detail(request, slug):
    post = get_object_or_404(_published_posts(), slug=slug)
    related_posts = _published_posts().exclude(pk=post.pk)
    if post.category_id:
        related_posts = related_posts.filter(category_id=post.category_id)
    return render(request, "blog/detail.html", {
        "post": post,
        "related_posts": related_posts[:3],
        "recent_posts": _published_posts().exclude(pk=post.pk)[:4],
    })
