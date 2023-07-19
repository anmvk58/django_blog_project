from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Author, Tag

all_posts = []
def get_date(post):
    return post["date"]

# Create your views here.
def starting_page(request):
    latest_post = Post.objects.all().order_by("-date")[:3]
    return render(request, 'blog/index.html', {
        "posts": latest_post
    })

def posts(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, 'blog/all-pages.html', {
        "posts": posts
    })

def post_detail(request, slug):
    # post = Post.objects.get(slug=slug)
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post-detail.html', {
        "post": post,
        "post_tags": post.tags.all()
    })