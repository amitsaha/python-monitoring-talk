from django.shortcuts import render
from django.http import (
    HttpResponseNotAllowed, HttpResponseRedirect,
    HttpResponseForbidden, HttpResponseNotFound,
)
from .models import Post, Tag, PostTag
from .forms import TilForm


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.views.decorators.cache import cache_page


def index(request):
    if not request.user.is_authenticated:
        latest_posts = Post.objects.filter(public=True).order_by('-post_date')[:5]
        return render(
            request, 'tilweb/index.html', {
                'posts': latest_posts
            })
    else:
        return HttpResponseRedirect('/me/')


def me(request):
    if request.user.is_authenticated:
        latest_posts = Post.objects.order_by('-post_date')
        post_tags = PostTag.objects.filter(
            post__in=[p for p in latest_posts]
        ).distinct()
        return render(
            request, 'tilweb/me.html', {
                'user': request.user,
                'posts': latest_posts,
                'tags': set([tag.tag for tag in post_tags]),
            })
    else:
        return HttpResponseRedirect('/login/')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/post/')
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'tilweb/login.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return HttpResponseRedirect('/post/')
            else:
                print('User not found')
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'tilweb/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/post/')
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'tilweb/signup.html', {'form': form})
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/post/')
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'tilweb/signup.html', {'form': form})


def create_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    elif request.method == 'GET':
        form = TilForm()
        latest_posts = Post.objects.filter(author=request.user).order_by('-post_date')[:5]
        return render(
            request, 'tilweb/create_post.html', {
                'form': form, 'posts': latest_posts
            })
    elif request.method == 'POST':
        form = TilForm(request.POST)
        if form.is_valid():
            p = Post(
                subject=form.cleaned_data.get('subject'),
                content=form.cleaned_data.get('content'),
                author=request.user,
                public=form.cleaned_data.get('public'),
            )
            p.save()
            tags = form.cleaned_data.get('tags')
            if tags:
                tags_list = tags.split(',')
                for tag in tags_list:
                    tag = tag.strip()
                    t = Tag.objects.filter(tag=tag)
                    if not t:
                        t = Tag(tag=tag)
                        t.save()
                    else:
                        t = t[0]
                    pt = PostTag(post=p, tag=t)
                    pt.save()

            return HttpResponseRedirect('/post/{0}/'.format(p.id))
        else:
            return render(
                request, 'tilweb/create_post.html', {
                    'form': form,
                })
    else:
        return HttpResponseNotAllowed('{0} Not allowed'.format(request.method))


@cache_page(60*15)
def show_post(request, post_id=None):
    post = Post.objects.filter(id=post_id)[0]
    # if the post is not public, only viewable by the author
    if not post.public:
        if not post.author == request.user:
            return HttpResponseForbidden()
    post_tags = PostTag.objects.filter(post=post)
    return render(request, 'tilweb/view_post.html', {
        'post': post,
        'tags': post_tags if len(post_tags) else None,
    })


def tag_view(request, tag):
    t = Tag.objects.filter(tag=tag)
    if t.all():
        t = t[0]
        posts = PostTag.objects.filter(tag=t)
        # Query all the public posts or the posts by
        # the currently logged in user with the
        # given tag
        posts = Post.objects.filter(id__in=[
            p.post.id for p in posts if p.post.public or
            p.post.author == request.user]
        )
        return render(request, 'tilweb/tag_view.html', {
            'tag': t.tag,
            'posts': posts,
        })
    else:
        return HttpResponseNotFound('<h1> Tag Not Found </h1>')
