from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count

from blog.models import Post, Category, User, Comment
from blog.forms import PostForm, CommentForm

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


class ProfileListView(ListView):
    model = User
    template_name = 'blog/profile.html'


class IndexListView(ListView):
    queryset = (
        Post
        .objects
        .prefetch_related('comments')
        .select_related('author')
        .filter(
            pub_date__lt=datetime.now(),
            is_published=True,
            category__is_published=True
        )
        .annotate(comment_count=Count('comments'))

    )
    paginate_by = 10
    template_name = 'blog/index.html'
    ordering = '-pub_date'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post_comment = post
        comment.save()
    return redirect('blog:post_detail', post_id=pk)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:post')
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:post')
    pk_url_kwarg = 'comment_id'