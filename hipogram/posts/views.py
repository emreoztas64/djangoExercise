from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post


def post_list_view(request):
    posts = Post.objects.all().order_by("-creation_datetime")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "post_list.html", {'posts': posts})

def create_view(request):
    return render(request, "create.html")

@login_required
def post(request):
    post = Post(
        image = request.FILES.get("image"),
        text = request.POST.get("text"),
        created_by = request.user
    )
    post.save()
    return redirect(reverse("posts:list"))