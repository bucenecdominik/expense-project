
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Item
from datetime import date, datetime
from .forms import ItemCreationForm

# Create your views here.
def index(request):
    user = request.user
    
    if not user: 
        return redirect('login_user')
    else:
        name = user.username
        item_list = Item.objects.all()
        return render(request, "index.html", {
        'item_list' : item_list,
        'name' : name,
        })


def delete_item(request, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()
    return render(request, 'index.html')

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
                'user' : user,
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
    pass
    
def money_spent_today(request):
    if request.method == 'POST':
        name = request.POST['item_name']
        description = request.POST['description']
        time_it_was_bought = datetime.now()
        price = request.POST['price']
        user = request.user
        item = Item.objects.create(name=name, description=description, time_it_was_bought=time_it_was_bought, price=price, user=user)
        item.save()
        items = Item.objects.filter(time_it_was_bought__date=date.today(), user = request.user)
        sum_price = sum(item.price for item in items)
        return render(request, 'money_spent_today.html', {
            'items' : items,
            'sum_price' : sum_price,
        })
    else:
        items = Item.objects.filter(time_it_was_bought__date=date.today(), user = request.user)
        sum_price = sum(item.price for item in items)
        return render(request, 'money_spent_today.html', {
            'items' : items,
            'sum_price' : sum_price,
        })

def money_spent_this_month(request):
    items = Item.objects.filter(time_it_was_bought__month = datetime.now().month, user = request.user)
    sum_price = sum(item.price for item in items)
    return render(request, 'money_spent_this_month.html', {
        'items' : items,
        'sum_price' : sum_price,
    })

def money_spent_this_year(request):
    items = Item.objects.filter(time_it_was_bought__year = datetime.now().year, user = request.user)
    sum_price = sum(item.price for item in items)

    return render(request, 'money_spent_this_month.html', {
        'items' : items,
        'sum_price' : sum_price,
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