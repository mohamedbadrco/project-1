from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Comment, Listing, User, Bid


CATEGORIES = (
    ("Fashion", "Fashion"),
    ("toys, hobby, and DIY. More", "toys, hobby, and DIY. More"),
    ("Electronics and media", "Electronics and media"),
    ("furniture and appliance", "furniture and appliance"),
)

CATEGORIES_L = ["Fashion","toys, hobby, and DIY. More","Electronics and media","furniture and appliance"]

#create add listing model
class NewListingForm(forms.Form):
    title = forms.CharField(label="listing title",widget= forms.TextInput(attrs={'class':'form-control'}))
    photo = forms.CharField(label="listing photo",widget= forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ChoiceField(choices = CATEGORIES,widget=forms.RadioSelect)
    starting_bid = forms.CharField(label="listing starting bid",widget= forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="listing description",widget = forms.Textarea(attrs={'class':'form-control','id':'text','rows':'20'}))

#index view load index page with all the active listings
def index(request):

    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.filter(active=True)
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


#add listing
def add_listing(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


    if request.method == "POST":
        form = NewListingForm(request.POST)
        #Ensure the from data is valid

        if form.is_valid():
            print(form.cleaned_data["starting_bid"])
            bid_1 = form.cleaned_data["starting_bid"]
            current_user = request.user
            #create model with form data

            listing = Listing.objects.create(owner=current_user,title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],photo=form.cleaned_data["photo"],
            category=form.cleaned_data["category"],starting_bid=int(bid_1)) 

            #redirct user to index view
            return HttpResponseRedirect(reverse("index"))

            
    form = NewListingForm()
    return render(request, "auctions/add_listing.html",{
        "form": form
        }
     )

#view listing
def view_listing(request, listing_id):
 
   

    listing = Listing.objects.get(pk=int(listing_id))
    

    if request.user.is_authenticated:
    #check if listing is in user watchlist 
        if listing in request.user.watchlist.all() :

            in_watchlist =True

        else:

            in_watchlist = False
    else:
        in_watchlist = False


    #load listing comments 
    comments = Comment.objects.filter(Listing=listing_id)

    return render(request, "auctions/view_listing.html",{
        "listing": listing,
        "user": request.user ,
        "comments": comments,
        "in_watchlist" : in_watchlist,
        #check if user is the owner of the listing
        "is_owner" : listing.owner == request.user

        })

#add bid 
def add_bid(request,listing_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


    if request.method == "POST":

        bid = request.POST["bid"]
        
        if not bid:
            return HttpResponse('invalid input')
        
        if not bid.isdigit():
            return HttpResponse('invalid input')

        

        current_user = request.user
         
        #fetch listing
        listing = Listing.objects.get(pk=int(listing_id))
        #fetch the listing bids 
        if Bid.objects.filter(Listing=int(listing_id)):
            largest_bid = Bid.objects.filter(Listing=int(listing_id)).order_by('-bid')[0]
        else:
            largest_bid = 0
        
        
        
         
        
        #check if bid is larger than listing starting bid 
        if int(bid) > listing.starting_bid:
            #check if the bid is larger than all other bids if there any other bids
            if largest_bid:
                if int(bid) > largest_bid.bid:
                    bid_op = Bid.objects.create(username=current_user,Listing=listing,bid=int(bid))
                    bid_op.save()
                    return HttpResponse('your bid was added successfully and now the highest bid on the item')
                else:
                    return HttpResponse('your bid is smaller than the largiest bid on this item so your bid wont be added')
            else:
                bid_op = Bid.objects.create(username=current_user,Listing=listing,bid=int(bid))
                bid_op.save()
                return HttpResponse('your bid was added successfully and now the highest bid on the item')
        else:
            return HttpResponse(f'your bid is smaller than the starting bid on this item')
            
    
#add comment
def add_comment(request,listing_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        comment = request.POST["comment"]
        current_user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment_op = Comment.objects.create(username=current_user,Listing=listing,comment=comment)
        comment_op.save
    return HttpResponseRedirect(f"{reverse(index)}listing/{listing_id}")

#add to watchlist
def add_watchlist(request,listing_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    current_user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(current_user)
    return HttpResponseRedirect(f"{reverse(index)}listing/{listing_id}")

#remove from watchlist
def remove_watchlist(request,listing_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    current_user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(current_user)
    return HttpResponseRedirect(f"{reverse(index)}listing/{listing_id}")


#view watchlist
def view_watchlist(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    current_user = request.user
    listings = Listing.objects.filter(watchlist=current_user)
    
    return render(request, "auctions/view_watchlist.html",{
        "listings":listings,
        "name" : current_user
        })

#view categories
def categories(request):
    return render(request, "auctions/categories.html",{
        "categories":CATEGORIES_L
        })

#view a category
def view_category(request,name):
    listings = Listing.objects.filter(category=name,active=True)
    return render(request, "auctions/view_category.html",{
        "listings": listings,
        "name":name
        })

#close listing
def close_listing(request,listing_id):

    listing = Listing.objects.get(pk=int(listing_id))

    if listing.owner == request.user:
        if Bid.objects.filter(Listing=listing.id):
            winning_bid = Bid.objects.filter(Listing=listing.id).order_by('-bid')[0]
        else:
            listing.active = False
            listing.save()
            return HttpResponse(f"{listing.title} was successfuly closed and User with no bids")



        listing.winner = winning_bid.username

        listing.active = False

        listing.save()
        
        return HttpResponse(f"{listing.title} was successfuly closed and User { winning_bid.username.username } had the highest bid")

    return HttpResponse("failed to close listing")