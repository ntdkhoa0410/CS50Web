import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.defaulttags import register
from .models import User, Post, Following_System


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    return render(request, "network/index.html")

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    currentUser_followings = Following_System.objects.get(user=currentUser).following
    allPosts = Post.objects.all().order_by("-timestamp").reverse()
    followingPosts = []
    for user in currentUser_followings.all():
        for post in allPosts:
            if post.author == user:
                followingPosts.append(post)
    
    post_likers_ids = {post.id: list(post.likers.values_list('id', flat=True)) for post in followingPosts}

    # Show 10 posts per page.
    paginator = Paginator(followingPosts, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html",{
        "page_obj": page_obj,
        "post_likers_ids" : post_likers_ids
    })

def edit (request,post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "PUT":
        post.content = json.loads(request.body)["changed_data"]
        print(json.loads(request.body)["changed_data"])
        post.save()
    return HttpResponse(status=204)

def like_update(request):
    if request.method == "PUT":
        post_id = json.loads(request.body)["post_id"]
        currentUser_Id = json.loads(request.body)["currentUser_Id"]
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=currentUser_Id)
        post.likers.add(user)
        post.save()
    return HttpResponse(status=204)

def unlike_update(request):
    if request.method == "PUT":
        post_id = json.loads(request.body)["post_id"]
        currentUser_Id = json.loads(request.body)["currentUser_Id"]
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=currentUser_Id)
        post.likers.remove(user)
        post.save()
    return HttpResponse(status=204)

def unfollow(request):
    userfollow_id = request.POST['userfollow']
    userfollow= User.objects.get(pk=userfollow_id)
    currentUser = User.objects.get(pk=request.user.id)
    currentUser_followings = Following_System.objects.get(user=currentUser).following
    currentUser_followings.remove(userfollow)
    return HttpResponseRedirect((reverse(profile,kwargs={'user_id':userfollow_id})))

def follow(request):
    userfollow_id = request.POST['userfollow']
    userfollow= User.objects.get(pk=userfollow_id)
    currentUser = User.objects.get(pk=request.user.id)
    currentUser_followings = Following_System.objects.get(user=currentUser).following
    currentUser_followings.add(userfollow)
    return HttpResponseRedirect((reverse(profile,kwargs={'user_id':userfollow_id})))

def allPosts(request):
    # Get all posts data - json
    allPosts = Post.objects.all()
    # Return emails in reverse chronologial order
    allPosts = allPosts.order_by("-timestamp").all()
    # Show 10 posts per page.
    paginator = Paginator(allPosts, 3) 
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    # return json all posts
    data = {
        'posts': [post.serialize() for post in page_obj],
        'page': {
            'has_previous': page_obj.has_previous(),
            'previous_page': page_obj.has_previous() and page_obj.previous_page_number() or None,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
            'num_pages' : page_obj.paginator.num_pages,
            'current_page' : page_number
        },
        'currentUser_Id' : request.user.id
    }
    return JsonResponse(data, safe=False)

def profile(request, user_id):
    # Get user data
    userProfile = User.objects.get(pk=user_id)
    # Return emails in reverse chronologial order of that user
    allPosts = Post.objects.filter(author=userProfile).order_by("-timestamp").reverse()
    # Show 10 posts per page.
    paginator = Paginator(allPosts, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Follow numbers
    followings = Following_System.objects.get(user=userProfile)
    followers = userProfile.following.all()
    if not followings:
        following_count = 0
    else:
        following_count = followings.following.all().count()
    followers_count = followers.count
    # Check if the user has follow or not
    try:
        currentUser = User.objects.get(pk=request.user.id)
        currentUser_followings = Following_System.objects.get(user=currentUser)
        if currentUser_followings.following.filter(pk=user_id):
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    post_likers_ids = {post.id: list(post.likers.values_list('id', flat=True)) for post in allPosts}
    return render(request, "network/profile.html",{
        "allPosts": allPosts,
        "page_obj": page_obj,
        "userProfile" : userProfile,
        "following_count" : following_count,
        "followers_count" : followers_count,
        "isFollowing" : isFollowing,
        "post_likers_ids" : post_likers_ids
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        new_Following_Systems = Following_System(user=user)
        new_Following_Systems.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Add new post to database
def createPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        author = User.objects.get(pk=request.user.id)
        newPost = Post(author=author, content=content)
        newPost.save()
    return HttpResponseRedirect(reverse("index"))