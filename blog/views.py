from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from blog.forms import PostForm
from blog.models import Post
from django.utils import timezone

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                User = get_user_model()
                user = User.objects.filter(is_active=True).first()
                if user is None:
                    user = User.objects.create_user(username="anon")
                post.author = user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                User = get_user_model()
                user = User.objects.filter(is_active=True).first()
                if user is None:
                    user = User.objects.create_user(username="anon")
                post.author = user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
