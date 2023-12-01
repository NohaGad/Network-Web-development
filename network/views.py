import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from .models import User, UserFollowing, Post


def index(request):
    return render(request, "network/index.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def post_view(request):
    
    if request.method == "GET":
        page_number = request.GET.get('page',1)
        items_per_page = 10
        posts = Post.objects.all().order_by('-created_at')

        username = request.GET.get('username', None)
        following = request.GET.get('following', None)
        if username:
            try:
                owner = User.objects.get(username=username)
                posts = posts.filter(owner=owner)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid username'}, status=400)

        if following:
            following_user_ids = UserFollowing.objects.filter(user_id=request.user).values_list('following_user_id', flat=True)
            posts = posts.filter(Q(owner__in=following_user_ids))


        paginator = Paginator(posts, items_per_page)

        try:
            current_page = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({'status': 'error', 'message': 'Invalid page number'}, status=400)

        serialized_posts = [post.serialize() for post in current_page]

        data = {
            'status': 'success',
            'data': serialized_posts,
            'has_next': current_page.has_next(),
            'has_previous': current_page.has_previous(),
            'total_pages': paginator.num_pages,
            'current_page': current_page.number,
        }
        return JsonResponse(data, safe=False)
        

    elif request.method == "POST": 
        data = request.POST
        post_text = data.get("post_text", "")

        if post_text == [""]:
            return JsonResponse({"error": "you must write anything before submit"}, status=400)
        else:
            post = Post()
            post.owner = request.user
            post.post_text = post_text
            post.save()
            return JsonResponse({"message": "Posted successfully."}, status=201)

@login_required
def follow_view(request):
    if request.method == "GET":
        user = request.user
        following_count = UserFollowing.objects.filter(user_id=user).count()
        followers_count = UserFollowing.objects.filter(following_user_id=user).count()
        data = {
            'status': 'success',
            'following_count': following_count,
            'followers_count': followers_count
         }
        return JsonResponse(data)
