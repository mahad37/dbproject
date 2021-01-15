from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listings, User, Comments, Bids, Transactions,Test
import datetime
from django.db import connection
import datetime


#with connection.cursor() as cursor:
        #cursor.execute("create view test2 as select id, title from auctions_listings")
 #       cursor.execute("drop view sum")
 #with connection.cursor() as cursor:
     #   cursor.execute("create view test1 as select id, user from auctions_comments")
        #summary=cursor.execute("select * from test1")
    #with connection.cursor() as cursor2:
    #summary=Test.objects.raw("select * from test2")

def index(request):
    all_listings= Listings.objects.raw("select * from auctions_listings order by date")
    summary=None
    return render(request, "auctions/index.html",
    {
    "all_listings": all_listings,"message":"All Listings"
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

def listing(request):
    if request.method=="POST":
        listing=Listings()
        listing.created_by=request.user
        listing.title=request.POST["title"]
        listing.description=request.POST["description"]
        listing.date=datetime.datetime.now()
        listing.starting_bid=request.POST["bid"]
        listing.Categories=request.POST["optradio"]
        listing.image=request.FILES["image"]
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/listing.html")


def item(request,item):
    comments=[]
    comments=Comments.objects.raw("select * from auctions_comments where item_id_id=%s order by date",[item])
    
    x=item
    listing=Listings.objects.get(id=item)
    if str(listing.created_by) == str(request.user):
        button=True
    else:
        button=False

    highest_bid=listing.starting_bid
    for bid in Bids.objects.all():
        if highest_bid<bid.bid:
            highest_bid=bid.bid
    

    #if len(bids) > 1:
     #   highest_bid=max(bids.bid)
    #elif not bids:
     #   highest_bid=Listings.objects.get(id=item).starting_bid
    #else:
     #   highest_bid,=bids.bid
    
    winner=False
    if listing.highest_bidder==request.user:
        winner=True


    return render(request, "auctions/item.html",{
    "item":listing,"comments":comments, "highest_bid":highest_bid, "button":button,
    "winner":winner,
    })


def view_watchlist(request):
    listings=[]
    all_listings=Listings.objects.all()
    for list in all_listings:
        if list.watchlist == True:
            listings.append(list)

    return render(request, "auctions/random.html",{
    "watchlist": listings
    })

def change_watchlist(request, item):
    listing=Listings.objects.get(id=item)
    if listing.watchlist != True:
        listing.watchlist = True
    else:
        listing.watchlist=False
    listing.save()
    return render(request, "auctions/item.html",{
      "item":listing
        })

def categories(request):
    categories=[]
    listings=Listings.objects.all()
    for list in listings:
        if not list.Categories in categories:
            categories.append(list.Categories)
    return render(request, "auctions/categories.html",{
    "categories":categories
    })

def category_items(request,category):
    items=[]
    items=Listings.objects.raw("select * from auctions_listings where categories=%s",[category])
    return render(request, "auctions/index.html",{
    "all_listings":items, "message":category
    })

def comment(request, item):
    if request.method=="POST":
        listing=Listings.objects.get(id=item)

        new_comment=Comments()
        new_comment.comment=request.POST["comment"]
        new_comment.user=request.user
        new_comment.item_id=listing
        new_comment.date=datetime.date.today()
        new_comment.save()
    
    comments=Comments.objects.raw("select * from auctions_comments where item_id_id=%s order by date",[item])

    listing=Listings.objects.get(id=item)
    if str(listing.created_by) == str(request.user):
        button=True
    else:
        button=False


    bids=[]
    all_bids=Bids.objects.all()
    for bid in all_bids:
        if bid.item_id == item:
            bids.append(bid.bid)
    if not bids:
        highest_bid=Listings.objects.get(id=item).starting_bid
    elif len(bids) > 1:
        highest_bid=max(bids)
    else:
        highest_bid,=bids


    return render(request, "auctions/item.html",{
    "comments": comments, "item":listing, "highest_bid":highest_bid, "button":button,

    })

def placebid(request, item):
    bids=[]
    listing=Listings.objects.get(id=item)
    all_bids=Bids.objects.all()
    for bid in all_bids:
        if bid.item_id == item:
            bids.append(bid.bid)

    if not bids:
        highest_bid=Listings.objects.get(id=item).starting_bid
    elif len(bids)>1:
        highest_bid=max(bids)
    else:
        highest_bid,=bids
    if request.method=="POST":
        highest=listing.starting_bid
        for bid in Bids.objects.all():
            if highest<bid.bid:
                highest=bid.bid
        if int(request.POST["bid"])<=highest:
            return render(request, "auctions/error.html",{
                 "message": "Error: Bid should be larger than the current price"
                     })

        else:
            #new_bid=Bids()
            new_bid=request.POST["bid"]
            #new_bid.user=request.user
            #new_bid.item_id=listing
            #new_bid.save()
            highest_bid=new_bid
            with connection.cursor() as cursor:
                cursor.execute('insert into auctions_bids(user_id,bid,item_id_id) values(%s,%s,%s)',[request.user.id,new_bid,listing.id])
            
            listing.highest_bidder=request.user
            listing.save()

    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)


    return render(request, "auctions/item.html",{
    "comments": comments, "item":listing, "highest_bid":highest_bid
    })

def close_bid(request,item):
    #listing=Listings.objects.get(id=item)
    #listing.close_bid=True
    #listing.save()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE auctions_listings SET close_bid = True WHERE id = %s", [item])

    listing=Listings.objects.get(id=item)
    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)
    return render(request, "auctions/item.html",{
    "item":listing,"comments":comments

    })

#trigger="""
#CREATE or replace trigger t5
#before insert ON auctions_transactions
#begin
#insert into auctions_transactions(product,seller_id,buyer_id,date,city,postal,amount) values(%s,%s,%s,%s,%s,%s,%s)',[listing.title,listing.created_by.id,request.user.id,datetime.date.today(),city,postal,amount*1.05]
#end;
#"""

#with connection.cursor() as c:
#    c.execute(trigger)

def checkout(request,item,amount):
    listing=Listings.objects.get(id=item)
    user=request.user
    time=datetime.datetime.now()
    if request.method=="POST":
        listing=Listings.objects.get(id=item)
        city=request.POST["city"]
        postal=request.POST["postal"]
        with connection.cursor() as cursor:
            cursor.execute('insert into auctions_transactions(product,seller_id,buyer_id,date,city,postal,amount) values(%s,%s,%s,%s,%s,%s,%s)',[listing.title,listing.created_by.id,request.user.id,datetime.date.today(),city,postal,amount])
        return render(request, "auctions/successful.html",{
        "user":user, "time":time, "item":listing, "amount":amount})

    
    return render(request, "auctions/checkout.html",{
    "user":user, "time":time, "item":listing, "amount":amount})



#with connection.cursor() as cursor:
    #cursor.execute("create view view1 as select id, product , date, amount from auctions_transactions")
def viewtransactions(request):
    transactions=Test.objects.raw("select * from view1")
    return render(request, "auctions/mypurchases.html",{
    "transactions":transactions})