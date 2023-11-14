from django.urls import path

from . import views
from .views import ProfileDetailView

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<int:user_id>/', ProfileDetailView.as_view(), name='user'),
]
