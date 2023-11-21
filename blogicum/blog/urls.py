from django.urls import path

from .views import ProfileListView, IndexListView, PostDetailView
from .views import CategoryListView, PostCreateView, add_comment
from .views import CommentUpdateView, CommentDeleteView, PostUpdateView
from .views import PostDeleteView, ProfileUpdateView

app_name = 'blog'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('posts/create/',
         PostCreateView.as_view(),
         name='create_post'
         ),
    path('posts/<post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<post_id>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<post_id>/delete/',
         PostDeleteView.as_view(),
         name='delete_post'
         ),
    path('category/<category_slug>/',
         CategoryListView.as_view(),
         name='category_posts'
         ),
    path('profile/<username>/', ProfileListView.as_view(), name='profile'),
    path('profile/<username>/edit/',
         ProfileUpdateView.as_view(),
         name='edit_profile'
         ),
    path('posts/<post_id>/comment/', add_comment, name='add_comment'),
    path('posts/<post_id>/comment/<comment_id>',
         CommentUpdateView.as_view(),
         name='edit_comment'
         ),
    path('posts/<post_id>/comment/<comment_id>/delete_comment/',
         CommentDeleteView.as_view(),
         name='delete_comment'
         ),
]
