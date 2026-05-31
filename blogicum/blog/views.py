from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def published_posts():
    """Возвращает QuerySet постов, доступных для публикации.

    Пост считается доступным, если одновременно:
    - он опубликован (is_published=True),
    - дата публикации не позже текущего момента,
    - категория, к которой он относится, опубликована.
    """
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )


def index(request):
    """Главная страница — пять последних публикаций."""
    template = 'blog/index.html'
    posts = published_posts()[:5]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, id):
    """Страница отдельной публикации."""
    template = 'blog/detail.html'
    post = get_object_or_404(published_posts(), id=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница категории публикаций."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    )
    context = {'category': category, 'posts': posts}
    return render(request, template, context)
