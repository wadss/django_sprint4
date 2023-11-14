from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView

from blog.models import Post, Category, User

QUANTITY_POSTS = 5


def queryset_posts():
    return Post.objects.select_related(
        'category', 'author', 'location').filter(
            pub_date__lte=datetime.now(),
            category__is_published=True,
            is_published=True,
    )


def index(request):
    template = 'blog/index.html'
    posts_list = queryset_posts()[:QUANTITY_POSTS]
    context = {'post_list': posts_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    posts_list = get_object_or_404(
        queryset_posts(), pk=post_id)
    context = {'post': posts_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects,
        is_published=True,
        slug=category_slug
    )
    posts = queryset_posts().filter(
        category=category)
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = 