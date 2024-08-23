from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date

from .models import Post, Tag

def post_list_view(request, tag=None, username=None):
    tags = Tag.objects.filter(post__creation_datetime__date=date.today()).annotate(count=Count("post")).order_by("-count")[:5]
    if tag:
        posts = Post.objects.filter(tags__name=tag).order_by("-creation_datetime")
    elif username:
        posts = Post.objects.filter(created_by__username=username).order_by("-creation_datetime")
    else:
        posts = Post.objects.all().order_by("-creation_datetime")
    page_number = request.GET.get("page")
    paginator = Paginator(posts, 5)
    posts = paginator.get_page(page_number)
    return render(request, "post_list.html", {'posts': posts, 'tags': tags})
    
@login_required
def create_view(request):
    if request.method == "POST":
        post = Post(
        image = request.FILES.get("image"),
        text = request.POST.get("text"),
        created_by = request.user,
        )
        post.save()
        tags = request.POST.getlist("tags")
        post.tags.set(tags)
        return redirect(reverse("posts:list"))
    else:
        tags = Tag.objects.all()
        return render(request, "create.html", {'tags': tags})

@login_required
def update_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.created_by:
        return redirect(reverse("posts:list"))
    if request.method == "POST":
        post.text = request.POST.get("text")
        post.save()
        tags = request.POST.getlist("tags")
        post.tags.set(tags)
        return redirect(reverse("posts:list"))
    else:
        tags = Tag.objects.all()
        return render(request, "update.html", {'post': post, 'tags': tags})

    
@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.created_by:
        return redirect(reverse("posts:list"))
    else:
        post.delete()
        return redirect(reverse("posts:list"))