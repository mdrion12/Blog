from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm

def post_list(request):
    categoryQ = request.GET.get('category', None)
    tagQ = request.GET.get('tag', None)
    search_query = request.GET.get('q', None)

    if categoryQ:
        posts = Post.objects.filter(category__name=categoryQ)
    elif tagQ:
        posts = Post.objects.filter(tag__name=tagQ)
    else:
        posts = Post.objects.all()

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tag__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags
    })

def post_details(request, id):
    post = get_object_or_404(Post, id=id)

    comments = Comment.objects.filter(post=post)
    like_count = Like.objects.filter(post=post).count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post_details.html', {
        'post': post,
        'comments': comments,
        'like_count': like_count,
        'user_liked': user_liked,
        'categories': categories,
        'tags': tags
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})


@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to update this post.')
        return redirect('post_details', id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_create.html", {"form": form})


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_details', id=post.id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('post_list')


@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        commenter = request.POST.get("comment")
        if commenter:
            Comment.objects.create(post=post, commenter=commenter)
    return redirect('post_details', id=post.id)


@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # toggle unlike
    return redirect('post_details', id=post.id)