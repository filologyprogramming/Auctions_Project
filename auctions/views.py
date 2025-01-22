from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Watchlist, Comment, Bid
from .models import User
from datetime import datetime
import json
from django.core.paginator import Paginator


# Shows index page with all listings
def index(request):
    listings = Listing.objects.all().order_by("-date")
    if not listings:
        return render(request, "auctions/error.html")
    
    # Create paginator
    paginator = Paginator(listings, 10)
    print(listings)
    # Get page number
    page_number = request.GET.get("page")
    # Create page object
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/index.html", {
        "page_obj": page_obj,
        "navbar": True
    })

# Login-in a user
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
        return render(request, "auctions/login.html", {
            "navbar": True
        })


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
                "message": "Passwords must match.",
                "navbar": True
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "navbar": True
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "navbar": True
        })


# Show and process a create listing form
@login_required(login_url='login')
def create(request):
    # Show a create listing form
    if request.method == "GET":
        # Get an empty create listing form
        form = ListingForm()
        if not form:
            error = "Can't retrieve a create listing form"
            return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
        else:
            return render(request, "auctions/create.html", {
                "form": form,
                "navbar": True
            })
    else:
        # Get form filled with data provided by a user
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # Get data from form
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"] 
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            condition = form.cleaned_data["condition"]
            category = form.cleaned_data["category"]
            date = datetime.now()
            seller = request.user
            listing = Listing(
                name=name, 
                price=price,
                date=date, 
                description=description,
                image=image,
                condition=condition,
                category=category,
                seller = seller 
                )
            # Save data in database
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            error = "Submitted form is invalid"
            return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })


@login_required(login_url='login')
def show_listing(request, listing_id, listing_name):
    if request.method == "GET":
        # Get all data about a single listing
        listing = Listing.objects.get(id=listing_id)
        if not listing:
            error = "Can't retrieve listings"
            return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
        else:
            # Get empty comment form
            comment_form = CommentForm()

            # Get all comments related to a listing
            comments = Comment.objects.filter(listing=listing_id)

            # Get watchlist of a user (used to conditionally choose elements to be shown)
            try:
                watchlist = Watchlist.objects.get(user = request.user)
            except Watchlist.DoesNotExist:
                watchlist = None

            # Get 5 latest bids of a listing (used to conditionally choose elements to be shown)
            bids = Bid.objects.filter(listing=listing).order_by("-bid")[:5]
            if not bids:
                bids = None
                highest_bid = None
                highest_bid_plus_1 = None
            else:
                # Get highest bid QuerySet
                highest_bid_object = Bid.objects.filter(listing=listing).order_by("-bid").first()

                # Retrieve the heighest bid
                highest_bid = highest_bid_object.bid

                # Format highest bid to 2 decimal places
                highest_bid = round(float(highest_bid), 2)
                highest_bid_plus_1 = highest_bid + 0.01
                highest_bid = round(float(highest_bid), 2)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "comment_form": comment_form,
            "comments": comments,
            "bids": bids,
            "highest_bid": highest_bid,
            "highest_bid_plus_1": highest_bid_plus_1,
            "navbar": False
        })


def categories(request):
    if request.method == "GET":
        # Look into each tuple of categories (ENTER, Entertainment)
        # and get 2nd value(Entertainment)
        # Pass it to a value and html
        all_categories = [c for c in Listing.CATEGORIES_CHOICES]
        return render(request, "auctions/categories.html", {
            "all_categories": all_categories,
            "navbar": True
        })
    
def show_listing_categories(request):
        category = request.GET.get('data')
        if category is None:
            error = "Can't retrieve selected category"
            return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
        else:
            listings = Listing.objects.filter(active=True).filter(category=category).order_by("-date")
            if not listings:
                listings = None
                return JsonResponse({"listings": listings})
            else:
                # Get condition of each listing
                all_conditions = [c for c in Listing.CONDITION_CHOICES]                
                # print(all_conditions)
                # Get list of all possible conditions of listings
                # list_of_abbs = [cond[] for cond in all_categories]
                
                final_list = []
                for key in listings.values():
                    for condition in all_conditions:
                        #print(category)
                        # Amend condition within final list
                        # Good practice of making copies
                        if key["condition"] == condition[0]:
                            final_list.append(key)
                            key["condition"] = condition[1]
                            print(final_list)
                   # print(key)
                    #print(list_of_abbs)
                
                # Convert each instance in the QuerySet into a dictionary
                # Then convert the entire QuerySet into a list of those dictionaries.
                return JsonResponse({"listings": final_list})

@login_required(login_url='login')
def my_listings(request):
    if request.method == "GET":
        # Get user
        user = request.user
        user_listings = Listing.objects.filter(seller=user).order_by("-date")
        if not user_listings:
            user_listings = None
            return render(request, "auctions/my_listings.html", {
                "user_listings": user_listings,
                "navbar": True
            })
        else:
            # Create paginator
            paginator = Paginator(user_listings, 4)
            # Get page number
            page_number = request.GET.get("page")
            # Create page object
            user_listings = paginator.get_page(page_number)
            return render(request, "auctions/my_listings.html", {
                "user_listings": user_listings,
                "navbar": True
            })

@login_required(login_url='login')
def my_purchases(request):
    if request.method == "GET":
        # Get user
        user = request.user
        user_purchases = Listing.objects.filter(sold_to=user).order_by("-date")
        if not user_purchases:
            user_purchases = None
            return render(request, "auctions/my_purchases.html", {
                "user_purchases": user_purchases,
                "navbar": True
            })
        else:
            # Create paginator
            paginator = Paginator(user_purchases, 4)
            # Get page number
            page_number = request.GET.get("page")
            # Create page object
            user_purchases = paginator.get_page(page_number)
            return render(request, "auctions/my_purchases.html", {
                "user_purchases": user_purchases,
                "navbar": True
            })

@login_required(login_url='login')
def active_biddings(request):
    if request.method == "GET":
        # Get user
        user = request.user
        # Get bids where a user is bidder, check for unique values on listing column
        bids = Bid.objects.filter(bidder=user).values('listing').distinct()
        print(bids)
        if not bids:
            active_biddings = None
            return render(request, "auctions/active_biddings.html", {
                "active_biddings": active_biddings,
                "navbar": True
            })
        else:
            # Get listings on which user bids 
            active_biddings = Listing.objects.filter(id__in=bids)
            # Create paginator
            paginator = Paginator(active_biddings, 4)
            # Get page number
            page_number = request.GET.get("page")
            # Create page object
            active_biddings = paginator.get_page(page_number)

            return render(request, "auctions/active_biddings.html", {
                "active_biddings": active_biddings,
                "navbar": True
            })
    
    
@login_required(login_url='login')
def show_watchlist(request):
    if request.method == "GET":
        # Get a user's watchlist
        try:
            watchlist = Watchlist.objects.get(user = request.user)
        except Watchlist.DoesNotExist:
            # Pass empty watchlist, html conditionally uses it to change a heading
            return render(request, "auctions/watchlist.html", {
            "watchlist": None,
            "navbar": True
        })

        # Get listings from a user's watchlist
        listings = watchlist.listing.all().order_by("-date")
        # Create paginator
        paginator = Paginator(listings, 4)
        # Get page number
        page_number = request.GET.get("page")
        # Create page object
        listings = paginator.get_page(page_number)
        return render(request, "auctions/watchlist.html", {
            "watchlist": listings,
            "navbar": True
        })
    

@login_required(login_url='login')
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        try:
            # Get all data from fetch request
            data = json.loads(request.body)
            listing_id = data["listing_id"]
            if listing_id is None:
                error = "Listing doesn't exist"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            else:
                # Try to create a watchlist for a user if it doesn't exist
                watchlist, created = Watchlist.objects.get_or_create(user=request.user)
                listing = Listing.objects.get(id=listing_id)
                if not listing:
                    error = "No such listing"
                    return render(request, "auctions/error.html", {
                    "error": error,
                    "navbar": True
                })
                # Add new listing to a watchlist
                # Creates a new relationship between listing <> watchlist
                watchlist.listing.add(listing)
                return JsonResponse({'message': 'Listing added to watchlist'})
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='login')
def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        try:
            # Get all data from fetch request
            data = json.loads(request.body)
            listing_id = data["listing_id"]
            if listing_id is None:
                error = "Listing doesn't exist"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            else:
                # Get user's watchlist
                watchlist = Watchlist.objects.get(user=request.user)
                if not watchlist:
                    error = "Can't access the watchlist"
                    return render(request, "auctions/error.html", {
                    "error": error,
                    "navbar": True
                })
                listing = Listing.objects.get(id=listing_id)
                if not listing:
                    error = "Can't access the watchlist"
                    return render(request, "auctions/error.html", {
                    "error": error,
                    "navbar": True
                })
                # Remove new listing from a watchlist
                watchlist.listing.remove(listing)
                if watchlist.listing.count() == 0:
                    watchlist.delete()
                    print("The watchlist is empty and deleted")
                else:
                    print("The watchlist is not empty.")
                return JsonResponse({'message': 'Removed from watchlist'})
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='login')
def add_comment(request, listing_id):
    if request.method == "POST":
        try:
            # Get data from fetch request
            data = json.loads(request.body)
            listing_id = data["listing_id"]
            if not listing_id:
                return JsonResponse({"error": "Cannot retrieve the ID of the listing"}, status=400)
            comment_text = data["comment_text"]
            if not comment_text:
                return JsonResponse({"error": "No comment given"}, status=400)
            comment_text = comment_text.strip()
            if comment_text == None or comment_text == "":
                return JsonResponse({"error": "A comment cannot be empty"}, status=400)

            # Get listing where the comment will be added
            listing = Listing.objects.get(id=listing_id)
            if not listing:
                error = "Can't retrieve thevlisting"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            # Get user who adds a comment
            user = request.user
            # Create Comment object and save all data to it
            comment_obj = Comment(
                comment = comment_text,
                listing = listing,
                user = user,
                date = datetime.now()
            )
            # Save comment object
            comment_obj.save()
            return JsonResponse({'message': 'Comment saved'})
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='login')
def place_a_bid(request, listing_id):
    if request.method == "POST":
        try:
            # Get all data from 
            data = json.loads(request.body)
            listing_id = data["listing_id"]
            if listing_id is None:
                error = "Can't retrieve listing ID"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })

            placed_bid = data["bid"]
            if placed_bid is None or placed_bid == "":
                error = "Can't retrieve a new bid"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            
            # Format placed bid to 2 decimal places
            placed_bid = round(float(placed_bid), 2)

            # Get initial price
            listing = (Listing.objects.get(id=listing_id))
            if not listing:
                error = "Can't retrieve listing"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            # Check if bidder is not the seller (ensures no artificial prce bumping)
            bidder = request.user
            if bidder == listing.seller:
                error = "You can't bid on your own item"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })

            # Get original price
            initial_price = listing.price
            initial_price = float(initial_price)
            
            # Get highest price
            heighest_price = 999999999999.99
            if placed_bid <= initial_price or placed_bid > heighest_price or placed_bid < 0:
                error = "Bid is either too high, lower than initial price or lower than zero"
                return render(request, "auctions/error.html", {
                "error": error,
                "navbar": True
            })
            
            # Ensure the bid is positive
            placed_bid = abs(placed_bid)

            # Try to retrieve all bids
            bids = Bid.objects.filter(listing=listing)

            # If bids don't exist
            if not bids:
                # Compare a new bid with initial price
                if placed_bid <= initial_price:
                    # Show error message if it's equal or lower than initial prize
                    error = "New bid cannot be lower or equal to initial price"
                    return render(request, "auctions/error.html", {
                    "error": error,
                    "navbar": True
            })
                # If new bid is higher than initial prize, add it
                else:
                    new_bid = Bid (
                    bid = placed_bid,
                    bidder = request.user,
                    listing = listing
                    )
                    new_bid.save()
                    return JsonResponse ({"message": "Bid placed"})
            else:
                # If bids already exist get QuerySet with the highest bid
                highest_bid_object = Bid.objects.filter(listing=listing).order_by("-bid").first()

                # Retrieve the highest bid number
                highest_bid = highest_bid_object.bid

                # Format highest bid to 2 decimal places
                highest_bid = round(float(highest_bid), 2)
                print(highest_bid)
                if placed_bid <= highest_bid:
                    error = "New bid cannot be lower or equal the highest bid"
                    return render(request, "auctions/error.html", {
                    "error": error,
                    "navbar": True
                })
                else:
                    new_bid = Bid (
                    bid = placed_bid,
                    bidder = request.user,
                    listing = listing
                )
                new_bid.save()

            return JsonResponse ({"message": "Bid placed"})

        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        

@login_required(login_url='login')
def close_listing(request, listing_id):
    if request.method == "POST":
        # Get listing ID
        listing_id = request.POST["listing_id"]
        # Get user(in this case owner of listing)
        user = request.user
        # Get the whole listing
        listing = Listing.objects.get(id=listing_id)
        if not listing:
            error = "Cannot retrieve the listing"
            return render(request, "auctions/error.html", {
            "error": error,
            "navbar": True
        })

        # Get highest bid and the owner of the bid
        highest_bid_object = Bid.objects.filter(listing=listing).order_by("-bid").first()
        if not highest_bid_object:
            listing.active = False
            listing.save()
            return redirect('show_listing', listing_id=listing_id, listing_name=listing.name)
    
        # Get the highest bid on a listing
        highest_bid = highest_bid_object.bid
        if not highest_bid:
            error = "No bids made"
            return render(request, "auctions/error.html", {
            "error": error,
            "navbar": True
        })

        # Get who bid the highest
        highest_bidder = highest_bid_object.bidder

        # Update the listing
        listing.sold_for = highest_bid
        listing.sold_to = highest_bidder
        listing.active = False
        listing.save()
        return redirect('show_listing', listing_id=listing_id, listing_name=listing.name)