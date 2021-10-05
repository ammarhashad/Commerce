from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listings,Bid,Comment
import datetime
from django.db import models


categories = ["Electronics", "Gaming", "Cameras", "Computers", "Furniture", "Books", "Art", "Beauty", "Clothes"]


def index(request):
    products = Listings.objects.filter(close=False)

    return render(request, "auctions/index.html",{
        "products":products
    })

def All(request):
    products = Listings.objects.all()

    return render(request, "auctions/index.html",{
        "products":products
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
        username = request.POST["username"].capitalize()
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

@login_required()
def create(request):
    product = Listings()
    if request.method == "POST":
        product.title = request.POST["title"]
        product.description = request.POST["details"]
        if request.POST["image_url"] == "":
            product.image_url = "https://www.mhlontlolm.gov.za/img/departments/municipalmanager/no_image.png"
        else:
            product.image_url = request.POST["image_url"]
        product.category = request.POST.getlist('category')
        product.starting_bid = request.POST["starting_bid"]
        print(request.user)
        product.user =  request.user
        product.save()
        # product.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html",{
        "categories" : categories
    })

def time_calculate(time):
    if time < 60:
        time = str(int(time)) +" secounds ago"
    elif (time // 60) < 60:
        time = str(int(time // 60)) +" mins ago"
    elif time // 3600 < 24:
        time = str(int(time // 3600)) +" hours ago"
    elif time // 86400 < 30:
        time = str(int(time // 86400)) +" days ago"
    elif time // 2419200 < 12:
        time = str(int(time // 2419200)) +" months ago"
    else:
        time = str(int(time // 29030400)) +" years ago"
    return time

def item(request, item_id, watch=False):
    item = Listings.objects.get(id=item_id)
    all_bids = item.bids.all()
    watchlists = item.Watchlist.all()
    print(all_bids)
    current_bid = item.starting_bid
    bid_time = 0
    # for bids
    if all_bids:
        # time
        time_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone()
        bid_time = time_now - all_bids[len(all_bids) - 1 ].bid_date
        bid_time = bid_time.total_seconds()
        bid_time = time_calculate(bid_time)
        # bid value
        all_bids_values = [ x.bid for x in all_bids]
        # current_bid = all_bids[len(all_bids) - 1 ].bid
        # 3'yrt de 34an el admin moken ya3ml bid b qema az3'r mn el current_bid x 34an ab2a mot2kd eno lw
        # bawz el donya ana tamm msh ba5od a5r qema w 5als
        current_bid = max(all_bids_values)



    return render(request, "auctions/Listing_Page.html",{
        "item":item,
        "current_bid":current_bid,
        "bid_now":current_bid+.01,
        "bid_time":bid_time,
        "watch":watch,
    })

def bid(request, item_id):
    if request.POST:
        item = Listings.objects.get(id=item_id)
        all_bids = item.bids.all()
        add_bid = request.POST["add_bid"]
        current_bid = 0

        if all_bids:
            current_bid = all_bids[len(all_bids) - 1].bid

        if float(add_bid) < current_bid:
            print(1)
            print("here")
            return render(request, "auctions/bid_error.html",{
                "item":item
            })

        b = Bid.objects.create(
        bid=add_bid,
        )
        b.bid = add_bid
        b.Which_bid.add(item)
        b.how_bid.add(request.user)
        return HttpResponseRedirect(reverse("item" , kwargs={ 'item_id': item_id, "watch":0 }))


def comment(request, item_id):
    if request.POST:
        item = Listings.objects.get(id=item_id)
        comment = request.POST["comment"]
        c = Comment.objects.create(
        comment=comment,
        )
        c.comment = comment
        c.list_comment.add(item)
        c.how_comment.add(request.user)

        return HttpResponseRedirect(reverse("item" , kwargs={ 'item_id': item_id,"watch":0 }))

def watchlist_controll(request, item_id, value):
    item = Listings.objects.get(id=item_id)
    if value:
        item.Watchlist.add(request.user)
        watch = 1
    else:
        item.Watchlist.remove(request.user)
        watch = 3


    return HttpResponseRedirect(reverse("item" , kwargs={ 'item_id': item_id, 'watch':watch}))


def close(request, item_id):
    if request.POST:
        item = Listings.objects.get(id=item_id)
        item.close = True
        item.save()
        return HttpResponseRedirect(reverse("item" , kwargs={ 'item_id': item_id, "watch":0 }))


def watchlist(request):
    products = User.objects.get(pk=request.user.id).Watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "products":products
    })


def category(request, name):

    categories_list = categories
    if name in categories:
        return render(request, "auctions/category.html",{
            "category":name,
            "products":Listings.objects.filter(category__icontains=name)
        })

    return render(request, "auctions/category.html",{
        "categories":categories_list,
        "products":Listings.objects.all()
    })


def my_item(request):

    return render(request, "auctions/my_item.html",{
        "products":Listings.objects.filter(user=request.user)
    })
