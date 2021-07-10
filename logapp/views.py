from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    # validatation here
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    #you have objects in the database before you can test 
    #for how to test things
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw
    )

    messages.info(request, 'Account created! Please login.')
    return redirect('/')

def login(request):

    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'No user with this email exists.')
        return redirect('/')

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, 'Password for this user is incorrect.')
        return redirect('/')

    request.session['email'] = user.email
    request.session['user_id'] = user.id
    return redirect('/checklist')

def logout(request):

    request.session.clear()

    return redirect('/')






    