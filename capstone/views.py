from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from .models import User, Place, PlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from serpapi import GoogleSearch
from django.core.paginator import Paginator
import requests

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
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


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
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

def index(request):
    return render(request, "capstone/index.html")

def view_states(request):
    states = Place.STATE_CHOICES
    return render(request, "capstone/view_states.html", {
        'states': states
    })

def state(request, state, category):
    user_places = Place.objects.filter(category=category, state=state)
    url = "https://api.foursquare.com/v3/places/search"

    params = {
        "query": category,
        "near": state,
        "limit": 50
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3bhv/Lz7GYSIIHMKUAonbbWcVFtCVIAdGak8YZLkD22M="
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        places = data.get("results", [])    

        paginator = Paginator(places, 10) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)    

        return render(request, "capstone/state.html", {
            "places": places,
            "state": state,
            "category": category,
            "page_obj": page_obj,
            "user_places": user_places
        })
    else:
        return HttpResponse("An error occurred while fetching data from the API.")


def states_categories(request, state):
    categories = Place.CATEGORY_CHOICES
    return render(request, "capstone/states_categories.html", {
        "state": state,
        "categories": categories
    })


def view_categories(request):
    categories = Place.CATEGORY_CHOICES
    return render(request, "capstone/view_categories.html", {
        "categories": categories
    })

def category(request, category):
    user_places = Place.objects.filter(category=category)

    url = "https://api.foursquare.com/v3/places/search"

    params = {
        "query": category,
        "near": "India",
        "sort": "POPULARITY",
        "limit": 50
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3bhv/Lz7GYSIIHMKUAonbbWcVFtCVIAdGak8YZLkD22M="
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        places = data.get("results", [])   

        paginator = Paginator(places, 10) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)     

        return render(request, "capstone/category.html", {
            "places": places,
            "category": category,
            "user_places": user_places,
            "page_obj": page_obj
        })
    else:
        return HttpResponse("An error occurred while fetching data from the API.")

@login_required
def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False) 
            place.user = request.user
            place.save()
            return render(request, "capstone/index.html")
    else:
        form = PlaceForm()

    return render(request, "capstone/add_place.html", {
        'form': form
        })

def user_place(request, id):
    place = Place.objects.get(id=id)
    map_location = get_location(place.name)
    place.map_location = map_location
    images = get_images(place.name)
    place.images = images
    return render(request, "capstone/user_place.html", {
        'place': place
        })

@login_required
def visit(request):
    places_to_visit = Place.objects.filter(is_to_visit=True)
    return render(request, 'capstone/visit.html', {
        'places_to_visit': places_to_visit
    })



def mark_place_to_visit(request, place_id):
    place = Place.objects.get(id=place_id)
    place.is_to_visit = True
    place.save()
    return render(request, 'capstone/visit.html')  


def view_place(request, place_id):
    url = f"https://api.foursquare.com/v3/places/{place_id}"


    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3bhv/Lz7GYSIIHMKUAonbbWcVFtCVIAdGak8YZLkD22M="
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        place = {
            "name": data.get("name", "N/A"),
            "address": data.get("location", {}).get("address", "N/A"),
            "category_name": data.get("categories", [])[0].get("name", "N/A"),
            "category_icon": data.get("categories", [])[0].get("icon", {}).get("prefix", ""),
            "latitude": data.get("geocodes", {}).get("main", {}).get("latitude", ""),
            "longitude": data.get("geocodes", {}).get("main", {}).get("longitude", ""),
        }

        images = get_images(place["name"], limit=7)
        place["images"] = images
        
        map_location = get_location(place["name"])
        place["map_location"] = map_location

        return render(request, "capstone/view_place.html", {
            "place": place,
            "place_id": place_id
        })
    else:
        return HttpResponse("An error occurred while fetching data from the API.")


def get_images(query, limit=3):
    params = {
        "q": query,
        "engine": "google_images",
        "ijn": "0",
        "api_key": "1ad22e9efb5c549100fcd40c1c1ede57fb6c9fe874b03c4c2e73bfb45b27bb3a",
        "num": limit
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results.get("images_results", [])
    limited_images = images_results[:limit]  # Limit the images to the desired number
    return limited_images

def get_location(query):
    params = {
        "q": query,
        "engine": "google_maps",
        "type": "search",
        "api_key": "1ad22e9efb5c549100fcd40c1c1ede57fb6c9fe874b03c4c2e73bfb45b27bb3a",
        "sort": "POPULARITY"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    search_metadata = results.get("search_metadata", {})
    google_maps_url = search_metadata.get("google_maps_url")
    return google_maps_url