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


# For no database, we have to create list post variables
# all_posts = []
# def get_date(post):
#     return post["date"]

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
    def check_post_save(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        # post = Post.objects.get(slug=slug)
        post = get_object_or_404(Post, slug=slug)

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "save_for_later": self.check_post_save(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        # post = Post.objects.get(slug=slug)
        post = get_object_or_404(Post, slug=slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "form": form,
            "comments": post.comments.all().order_by("-id"),
            "save_for_later": self.check_post_save(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")

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
