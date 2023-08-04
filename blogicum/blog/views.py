from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.http import Http404, HttpResponseForbidden

from .forms import PostForm, CommentForm, UserForm
from blog.models import Post, Category, Comment


NUM_OF_PUB = 5
PAGINATE_BY = 10


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"


def get_queryset_vis_pub():
    return (
        Post.objects.filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by("-pub_date")
        .select_related("author", "category", "location")
        .annotate(comment_count=Count("comments"))
    )


class PostListView(PostMixin, ListView):
    template_name = "blog/index.html"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return get_queryset_vis_pub()


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    success_url = reverse_lazy("blog:index")
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author.id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def handle_no_permission(self):
        return redirect("login")


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs["pk"])
        if instance.author != request.user and instance.is_published is False:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        context["form"] = CommentForm()
        context["comments"] = post.comments.select_related("author")
        return context


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs["pk"])
        if instance.author != request.user:
            return redirect(
                reverse("blog:post_detail", kwargs={"pk": instance.pk})
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


def profile_detail(request, username):
    template = "blog/profile.html"
    profile = get_object_or_404(User, username=username)
    posts = (
        Post.objects.all()
        .annotate(comment_count=Count("comments"))
        .filter(
            author__username=username,
        )
        .order_by("-pub_date")
    )

    if not (
        request.user.is_authenticated and request.user.username == username
    ):
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )

    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"profile": profile, "page_obj": page_obj}
    return render(request, template, context)


@login_required
def edit_profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.POST.get("username"))
    return render(request, "blog/user.html", {"form": form})


class IndexListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return get_queryset_vis_pub()


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_queryset_vis_pub().filter(category=category)
    paginator = Paginator(post_list, PAGINATE_BY)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"category": category, "page_obj": page_obj}
    return render(request, template, context)


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs["post_id"]}
        )


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pk_url_kwarg = "comment_id"

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs["post_id"]}
        )

    def dispatch(self, request, *args, **kwargs):
        comment_update = get_object_or_404(Comment, pk=kwargs["comment_id"])
        if comment_update.author != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pk_url_kwarg = "comment_id"

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs["post_id"]}
        )

    def dispatch(self, request, *args, **kwargs):
        comment_delete = get_object_or_404(Comment, pk=kwargs["comment_id"])
        if comment_delete.author != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
