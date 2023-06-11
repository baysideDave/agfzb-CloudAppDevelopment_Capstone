from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
from .restapis import *
from .restapis import get_request, get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import sys, os
from pprint import pprint

# Getting a logger instance
logger = logging.getLogger(__name__)


# Create your views here.  


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `index` view to return a static index page
def index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)



# Create a `login_request` view to handle sign in request
# IMPORTANT - this view uses the index.html template - it does not have
# it's own template. It will indicate a bad login attempt on the index page, and it will
# show the user as logged in when sucessful

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST
        username = request.POST['f1_username']
        password = request.POST['f1_psw']
        # Try to check if the provided credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to do actual login
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            #the bad case - tell the user input was bad on the return to login page
            context["message"]="The Username or password you entered was incorrect - Please try again"
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)
    


# `logout_request` this view is used to handle sign a out request
# IMPORTANT - this view uses the index.html template by redirecting to /djangoapp - it does not have
# it's own template. It will indicate that no user is logged in on the index.html template
# 
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to index page
    return redirect('/djangoapp')

    

# `registration_request` view  - handles a sign up request
# from the nav-bar
# NOTE - this vuew has it's own template but whwn unsucessful sends a message to the
#        index page, and when sucessful, redireccts to the idex page which will show
#        the newly registered user logged in
#
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['reg-username']
        password = request.POST['reg-psw']
        first_name = request.POST['reg-firstname']
        last_name = request.POST['reg-lastname']
        user_exist = False
        try:
            # Check to see if the user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not an an existing user, we will log the username as a new user for debug purposes
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Add the new user to th auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to the index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"]="Account could not be created try again."
            return render(request, 'djangoapp/registration.html', context)




# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/dealership"
        # Get the dealers calling a function that will use a web action
        dealerships = get_dealers_from_cf(url)
        print("dealers form cf = ", dealerships[2])
        # add the returned data to context
        context["dealership_list"] = dealerships

        # old test code
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        
        return render(request, 'djangoapp/index.html', context)
        
"""
    def get_dealerships(request):
        context = {}
        if request.method == "GET":
            return render(request, 'djangoapp/index.html', context)
"""
"""
def get_dealerships(request):
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        #  mine  url = "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/get-dealership"
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
"""
"""
def get_dealerships(request):
    if request.method == "GET":
        context = {}

        state = request.GET.get("st")
        dealerId = request.GET.get("dealerId")
        #their url
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-dealership"

        # url below is mine
        #url =  "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/get-dealership"

        try:
            if state:
                dealerships = get_dealers_from_cf(url, st=state)
            elif dealerId:
                dealerships = get_dealers_from_cf(url, dealerId=dealerId)
            else:
                dealerships = get_dealers_from_cf(url)
        except Exception as e:
            # Handle the error and set dealerships to an empty list or display an error message
            dealerships = []
            context["error"] = f"An error occurred while fetching dealerships: {e}"
            #my code
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealership_list"] = dealerships
        print(context["dealership_list"])
        
        
        return render(request, "djangoapp/index.html", context=context)

"""

#To be done


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
#...
def get_dealer_details(request, dealer_id):
    context={}
    reviews_url = "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/review"
    dealer_name_url = "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/dealership"
    #   apikey="<cloudant key goes here>"
    #
    # be sure to set up environmental value on the os level - see next line
    # export APIKEY=<your value goes here, without the angle brackets>
    apikey = os.environ.get('APIKEY')

    # getting the dealer name
    dealer_name = get_dealer_name_by_id_from_cf(dealer_name_url, dealerId=dealer_id)
    print("dealer name is: ", dealer_name)
    context["dealer_name"] = dealer_name

    # dsg print("dealer is ",dealer_id)
    # Get dealers from the URL
    reviews = get_dealer_reviews_from_cf(reviews_url,dealer_id)
    #print("back in get_dealer_details: reviews = ", reviews[0])
    #pprint(reviews[0])
    
    context["dealer_id"]=dealer_id
    context["reviews"]=reviews
    

    # Concat all reviewers names - old test code
    #reviewer_names = ' '.join([reviewer.name for reviewer in dealer_details])
    # Return a list of reviewer names
    #return HttpResponse(reviewer_names)

    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

# View to submit a new review
#def add_review(request, dealer_id):
def add_review(request, dealer_id):
    print("in add_review dealer_id = ",dealer_id)
    context={}
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            print("in add_review, get request dealer_id = ",dealer_id)
            #dealer_id = 7
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/dealership-package/dealership"

            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)

        # POST request posts the content in the review submission form to the Cloudant DB using the post_review Cloud Function
        if request.method == "POST":
            print("in add_review, post request")
            form = request.POST
            review = dict()
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.carmake
            review["car_model"] = car.name
            review["car_year"] = car.year
            
            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            print("in views.py add_review - structure is: ", review)
        
            url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/2b6849a1-8e21-482f-bf2f-f9a9fc3dd9b5/actions/dealership-package/post-review"
            print("in add_review - url = ", url)
            json_payload = {"review": review}  # Create a JSON payload that contains the review data
            print
            # Performing a POST request with the review
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("in add+review - Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    else:
        # for user who isn't logged in, redirect to login page
        print("redirecting user to login page.")
        return redirect("/djangoapp/login")
