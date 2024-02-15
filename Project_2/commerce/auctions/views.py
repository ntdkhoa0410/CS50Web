from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Catergory, Bid, Comment


def index(request):
    listings = Listing.objects.filter(isActive=True)
    categories = Catergory.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories" : categories,
        "categoryName" :"All categories"
    })

def display_specific(request):
    categoryName = request.POST["category"]  
    if categoryName == "All categories":
        listings = Listing.objects.filter(isActive=True)
    else:
        category = Catergory.objects.filter(catergory_name=categoryName)
        listings = Listing.objects.filter(isActive=True,category__in=category)
    categories = Catergory.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories" : categories,
        "categoryName" : categoryName
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        owner = request.user
        title = request.POST['title']
        description = request.POST['description']
        image_link = request.POST['image_link']
        starting_bid = request.POST['starting_bid']
        category_name = request.POST['category']
        category = Catergory.objects.get(catergory_name=category_name)
        bid = Bid(bid=starting_bid, user=request.user)
        bid.save()
        new_listing = Listing(
            title=title,
            owner = owner,
            description=description,
            image_link = image_link,
            bid_price = bid,
            category = category
        )

        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Catergory.objects.all()
        return render(request, "auctions/create.html",{
            "categories":categories
        })
    
def details(request,id,title):
    listing = Listing.objects.get(pk=id)
    users = listing.watch_list.all()
    comments = Comment.objects.filter(listing=listing)
    inUserWatchlist = request.user in users
    isOwner = request.user == listing.owner
    return render(request,"auctions/details.html",{
        "listing" : listing,
        "inUserWatchlist" :inUserWatchlist,
        "comments" : comments,
        "isOwner" : isOwner
    })

def removeWatchlist(request,id):
    data = Listing.objects.get(pk=id)
    currentUser = request.user
    data.watch_list.remove(currentUser)
    return  HttpResponseRedirect(reverse("details", args=(id, data.title)))

def addWatchlist(request,id):
    data = Listing.objects.get(pk=id)
    currentUser = request.user
    data.watch_list.add(currentUser)
    return  HttpResponseRedirect(reverse("details", args=(id, data.title)))

def closeListing(request,id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("details", args=(id, listing.title)))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.watch_list.all()
    return render(request, "auctions/watchlist.html",{
        "listings" : listings
    })

def addBid(request,id):
    newBid = request.POST['bid']
    listing = Listing.objects.get(pk=id)
    bid = Bid(bid=newBid, user=request.user)
    bid.save()
    listing.bid_price = bid
    listing.save()
    return  HttpResponseRedirect(reverse("details", args=(id, listing.title)))

def addComment(request,id):
    currentUser = request.user
    listing = Listing.objects.get(pk=id)
    comment = request.POST['comment']
    newComment = Comment(
        writer = currentUser,
        listing = listing,
        comment = comment
    )
    newComment.save()
    return  HttpResponseRedirect(reverse("details", args=(id, listing.title)))

def inactiveListing(request):
    listings = Listing.objects.filter(isActive=False)
    return render(request, "auctions/inactiveListing.html", {
        "listings": listings,
    })
