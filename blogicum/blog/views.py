from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView)

from blog.models import Post, Category, User
from blog.forms import PostForm, CommentForm, UpdateProfileForm
from blog.mixins import SuccerUrlMixin, PostMixin, CommentMixin

PAGINATE_COUNT = 10


def get_posts_queryset(filter=False, comments=False):
    post_filter = (
        Post.objects
        .prefetch_related('comments')
        .select_related(
            'author',
            'location',
            'category',)
    )
    if filter:
        post_filter = post_filter.filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    if comments:
        post_filter = (
            post_filter.order_by('-pub_date')
            .annotate(
                comment_count=Count('comments')
            )
        )
    return post_filter


class ProfileListView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_COUNT

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context

    def get_queryset(self):
        author = self.get_author()
        return get_posts_queryset(
            filter=self.request.user != author,
            comments=True
        ).filter(author=author)


class ProfileUpdateView(LoginRequiredMixin, SuccerUrlMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = UpdateProfileForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class IndexListView(ListView):
    queryset = get_posts_queryset(filter=True, comments=True)
    paginate_by = PAGINATE_COUNT
    template_name = 'blog/index.html'
    ordering = '-pub_date'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    queryset = get_posts_queryset(filter=False, comments=False)

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author != self.request.user and (
            post.is_published is False
            or post.category.is_published is False
            or post.pub_date > timezone.now()
        ):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        )
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_COUNT

    def get_category(self):
        return get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug'],
        )

    def get_queryset(self):
        return get_posts_queryset(filter=True, comments=True).filter(
            category=self.get_category(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class PostCreateView(LoginRequiredMixin, SuccerUrlMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    success_url = reverse_lazy('blog:index')


class PostDeleteView(
        LoginRequiredMixin,
        PostMixin,
        SuccerUrlMixin,
        DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post_comment = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(
    LoginRequiredMixin,
    CommentMixin,
    UpdateView,
):
    form_class = CommentForm


class CommentDeleteView(
    LoginRequiredMixin,
    CommentMixin,
    DeleteView,
):
    pass
