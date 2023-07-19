from datetime import date
from typing import Any, Dict
from django.db.models.query import QuerySet

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Author, Tag
from django.views.generic import ListView, DetailView

all_posts = []
def get_date(post):
    return post["date"]


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostView(ListView):
    template_name = 'blog/all-pages.html'
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

class SinglePostView(DetailView):
    template_name = 'blog/post-detail.html'
    model = Post

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        return context

# Create your views here.
# Method belows is deprecated, Class inherit View/ListView above instead

# def starting_page(request):
#     latest_post = Post.objects.all().order_by("-date")[:3]
#     return render(request, 'blog/index.html', {
#         "posts": latest_post
#     })

# def posts(request):
#     posts = Post.objects.all().order_by("-date")
#     return render(request, 'blog/all-pages.html', {
#         "posts": posts
#     })

# def post_detail(request, slug):
#     # post = Post.objects.get(slug=slug)
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         "post": post,
#         "post_tags": post.tags.all()
#     })