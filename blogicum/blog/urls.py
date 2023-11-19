from django.urls import path

from . import views
from .views import ProfileListView, IndexListView, PostDetailView, CategoryDetailView, PostCreateView, add_comment, CommentUpdateView, CommentDeleteView

app_name = 'blog'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', CategoryDetailView.as_view(),
         name='category_posts'),
    path('profile/<username>/', ProfileListView.as_view(), name='profile'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/comment/<int:comment_id>', CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='delete_comment')
]
