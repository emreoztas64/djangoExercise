from django.db.models import Count
from datetime import date
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Tag

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag = self.kwargs.get("tag")
        username = self.kwargs.get("username")
        if tag:
            return Post.objects.filter(tags__name=tag).order_by("-creation_datetime")
        elif username:
            return Post.objects.filter(created_by__username=username).order_by("-creation_datetime")
        else:
            return Post.objects.all().order_by("-creation_datetime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.filter(post__creation_datetime__date=date.today()).annotate(count=Count("post")).order_by("-count")[:5]
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["image", "text", "tags"]
    template_name = "create.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["image", "text", "tags"]
    template_name = "update.html"
    success_url = "/"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            created_by=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"
    template_name = "delete.html"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            created_by=self.request.user
        )
