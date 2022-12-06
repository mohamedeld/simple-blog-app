from django.urls import path
from . import views

app_name = 'blog_app'
urlpatterns = [
    path("",views.StartingPage.as_view(),name='start'),
    path("posts",views.AllPosts.as_view(),name="posts"),
    path("posts/<slug:slug>",views.Post.as_view(),name="post"),
    path("read-later",views.ReadLater.as_view(),name="read-later"),
]
