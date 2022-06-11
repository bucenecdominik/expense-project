from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Item
from datetime import date, datetime

# Create your views here.

def index(request):
    item_list = Item.objects.all()
    
    return render(request, "index.html", {
        'item_list' : item_list
    })

def items(request):
    item_list = Item.objects.all()

    return render(request, "items.html", {
        'item_list': item_list,
    })

def delete_item(request):
    pass

#login the user  
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f"You have successfully logged in {username}")
            login(request, user)
            return render(request, 'index.html', {
                'name' : username,
            })
        else:
            messages.success(request, f"Logging in failed try again.")
            return redirect('login')
    else:
        return render(request, 'login.html')

#logouts the user
def logout_user(request):
    messages.success(request, f"You have succesfully logged out.")
    logout(request)
    return redirect('index')


#adds item to the database
def add_item(request):
    if request.method == 'POST':
        name = request.POST['item_name']
        description = request.POST['description']
        time_it_was_bought = datetime.now()
        price = request.POST['price']
        item = Item.objects.create(name=name, description=description, time_it_was_bought=time_it_was_bought, price=price)
        item.save()
        return render(request, "add_item.html")
    else:
        return render(request, "add_item.html")
    
def money_spent_today(request):
    items = Item.objects.filter(time_it_was_bought__date=date.today())

    return render(request, 'money_spent_today.html', {
        'items' : items
    })

def money_spent_this_month(request):
    items = Item.objects.filter(time_it_was_bought__month = datetime.now().month)

    return render(request, 'money_spent_this_month.html', {
        'items' : items
    })

def money_spent_this_year(request):
    items = Item.objects.filter(time_it_was_bought__year = datetime.now().year)

    return render(request, 'money_spent_this_month.html', {
        'items' : items
    })


def register_user(request): 
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('index')      
    else:  
        form = UserCreationForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'register.html', context) 