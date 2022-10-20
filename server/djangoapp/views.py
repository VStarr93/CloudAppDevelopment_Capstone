from operator import is_not
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
from .restapis import get_all_reviews, get_dealer_by_id, get_dealers_from_cf, \
    get_request, get_dealer_by_state, get_dealer_reviews_from_cf, \
    post_request, get_all_reviews
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render (request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        reenter_password = request.POST['reenter_password']
        user_exist = False
        # Check if passwords match
        if password == reenter_password:
            try:
                User.objects.get(username=username)
                user_exist = True
            except:
                logger.error("New user")
            if not user_exist:
                user = User.objects.create_user(username=username, first_name=first_name, 
                    last_name=last_name, password=password)
                login(request, user)
                return redirect('djangoapp:index')
            else:
                context['message'] = "User already exists."
                return render(request, 'djangoapp/registration.html', context)
        else:
            context['message'] = "Passwords do not match."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealerships'] = dealerships
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a get_dealer_by_id view
def get_dealer_by_id_view(request, id):
    # context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealer_by_id(url, id)
        # Concat all dealer's short name
        dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return render(request, 'djangoapp/index.html', context)
        return HttpResponse(dealer_names)
    
# Create a get_dealer_by_state view
def get_dealer_by_state_view(request, st):
    # context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealer_by_state(url, st)
        # Concat all dealer's short name
        dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return render(request, 'djangoapp/index.html', context)
        return HttpResponse(dealer_names)
# Create a `get_dealer_details' view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
# ...
    if request.method == "GET":
        context = {}
        reviewUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-review.json"
        reviews = get_dealer_reviews_from_cf(reviewUrl, dealerId=dealer_id)
        # Append a list of reviews to context
        context['reviews'] = reviews
        # Append dealer object to context
        dealershipUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-dealership.json"
        dealership = get_dealer_by_id(dealershipUrl, dealer_id)
        context['dealership'] = dealership
        context['dealerId'] = dealer_id
        # return a HttpResponse
        #return HttpResponse(context['reviews'])
        # redirect
        return render(request, 'djangoapp/dealer_details.html', context)
        
# Create a `add_review` view to submit a review
def add_review(request, dealerId):
    # first, authenticate the user
    if request.user.is_authenticated:
        # if request.method == 'POST':
        if request.method == 'POST':
            
            json_data = json.loads(request.body)
            # Create a dictionary object called review to append
            # keys like (time, name, dealership, review, purchase)
            # and any attributes you defined in your review-post cloud function
            # Example:
            # review["time"] = datetime.utcnow().isoformat()
            # review["dealership"] = 11
            # review["review"] = "This is a great car dealer"
            review = {}
            review['id'] = json_data['id']
            review['name'] = json_data['name']
            review['dealership'] = json_data['dealership']
            review['review'] = json_data['review']
            review['purchase_date'] = json_data['purchase_date']
            review['purchase'] = json_data['purchase']
            review['car_make'] = json_data['car_make']
            review['car_model'] = json_data['car_model']
            review['car_year'] = json_data['car_year']

            # Create another dictionary object called json_payload with one key
            # called review. like json_payload["review"]=review
            # the json_payload will be used as the request body
            json_payload = {}
            json_payload["review"] = review

            # Call the post_request method with the payload 
            # post_request(url, json_payload, dealerId=dealer_id)
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/post-review"
            result = post_request(url, json_payload)
            print(result)
            context = {}
            context["result"] = result
            # Return the result of post_request to add_review method
            # you may print the post response in console or append to HTTPResponse
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        
        # if request.method == 'GET'
        if request.method == 'GET':
            context = {}
            # query the cars with the dealer id to be reviewed
            # the queried cars will be used in the <select> dropdown
            cars = CarModel.objects.filter(dealer_id=int(dealerId))
            context["Cars"] = cars
            # add dealer_id to context
            context["dealerId"] =dealerId
            # add dealership to context
            dealerUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-dealership.json"
            dealer = get_dealer_by_id(dealerUrl, dealerId)
            context["dealer"] =dealer
            return render(request, 'djangoapp/add_review.html', context)
            # Configure the route for add_review view in urls.py
    else:
        return HttpResponse("You are not logged in")

# create a view to import cars from cloudant databases
def import_cars(request):
    # authenticate user
    if request.user.is_authenticated:
        # pull all reviews from cloudant
        getReviewsUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/912f86c9-d8b5-4c4d-8b16-5cdafae12178/dealership-package/get-review.json"
        reviews = get_all_reviews(getReviewsUrl)
        importedReviews = []
        for review in reviews:
            carMake = CarMake.objects.create(
                name=review.name,
                description="Imported from cloudant Database"
            )
            carModel = CarModel.objects.create(
                car_make=carMake,
                name=review.car_model,
                dealer_id=review.dealership,
                year=review.car_year
            )
            importedReviews.append(carModel)
        return HttpResponse(importedReviews)
    else:
        return HttpResponse("You are not logged in")