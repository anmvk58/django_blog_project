from datetime import date
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Author, Tag
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentForm
from django.urls import reverse

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

class SinglePostView(View):
    def get(self, request, slug):
        # post = Post.objects.get(slug=slug)
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags" : post.tags.all(),
            "form" : CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)
    
    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
    
        context = {
            "post": post,
            "post_tags" : post.tags.all(),
            "form" : CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

#
# This method deprecated because we need handle both get and post method !
#
# class SinglePostView(DetailView):
#     template_name = 'blog/post-detail.html'
#     model = Post

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         form = CommentForm()
#         context =  super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["form"] = form
#         return context


#
# Create your views here.
# Method belows is deprecated, Class inherit View/ListView above instead
#
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
