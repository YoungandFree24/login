from django.shortcuts import render, redirect
from .models import *
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import bcrypt

'''
renders the registration
# action method for index
'''

def index(request):
    return render(request, "home_page.html") 


def register(request):
    #check if it is post request
    if request.method == "POST":
        # check if register object is valid
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/')
        #check to see if email if user email is in use
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request,"Email is already in use.",extra_tags="email")
            return redirect('/')

        #Hash the password with Brcpyt
        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        #create User in Database
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )

    #put user id into session and redirect
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')
    else:
        return redirect('/')

def login(request):
    # Check if POST REquest
    if request.method == "POST":
        #  validate login object coming in
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                print(value)
                messages.error(request,value, extra_tags=key)
            return redirect('/')

    #check to see if email is correct
        user = User.objects.filter(email=request.POST['login_email'])
        # if email doesn't exist
        if len(user) == 0:
            messages.error(request,"Invalid Email/Password", extra_tags="login")
            return redirect('/')

        # checks if passwords match
        # returns boolean if true we continue on, if false we send error message
        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request,"Invalid Email/Password", extra_tags="login")
            return redirect('/')

        #  Put UserID into session and redirect
        request.session['user_id'] = user[0].id
        return redirect('/dashboard')
    else:
        return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'dashboard.html', context)

# the logout function  clears out session and redicts to homepage
# remember in django if you delete something not in session we will get an error
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

# def books(request):
#     context = {
#         "all_the_books": Book.objects.all(),
#         "all_the_authors": authors.objects.all()
#     }
#     return render(request, "book.html", context)