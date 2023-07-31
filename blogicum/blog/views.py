from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.db.models import Count

from .forms import PostForm, CommentForm
from blog.models import Post, Category, Comment


NUM_OF_PUB = 5
PAGINATE_BY = 10


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class PaginatorMixin:
    paginate_by = 10


class PostListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
            ).order_by('-pub_date').annotate(comment_count=Count("comments"))
        return queryset


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username}
                       )


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author.id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def handle_no_permission(self):
        return redirect('login')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user and instance.is_published is False:
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            post.comments.select_related('author')
            )
        return context


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect(reverse(
                'blog:post_detail',
                kwargs={'pk': instance.pk})
                )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class ProfileListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATE_BY
    template_name = 'blog/profile.html'

    def func(self):
        return self.request.user.username == self.kwargs['username']

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = Post.objects.filter(
            author__username=username
            ).order_by('-pub_date').annotate(comment_count=Count("comments"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        profile = User.objects.get(username=username)
        post_list = Post.objects.filter(author=profile).order_by('-pub_date')
        paginator = Paginator(post_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["profile"] = profile
        context["page_obj"] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('blog:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


def get_queryset_vis_pub():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return get_queryset_vis_pub().filter(
            category__is_published=True
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(
        is_published=True, slug=category_slug))
    page_obj = get_queryset_vis_pub().filter(
        category__slug=category_slug).select_related(
        'category', 'location', 'author').order_by('-pub_date').annotate(
        comment_count=Count('comments'))

    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
            )


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['post_id']})
