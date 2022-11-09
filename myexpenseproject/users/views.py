
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import StandingOrderForm, UserUpdateForm
from .models import Item, StandingOrder
from datetime import date, datetime
from .filters import ItemFilter
from django.views.generic import *
from .forms import ItemForm



# Create your views here.
class IndexView(View):
    def get(self, request):
        user = request.user
        if not user: 
            return redirect('login_user')
        else:
            name = user.username
            item_list = Item.objects.all()
            order_list = StandingOrder.objects.all()
            sum_price = sum(item.price for item in item_list)
            budget = 1200000 - sum_price
            return render(request, "index.html", {
            'order_list': order_list,
            'item_list' : item_list,
            'name' : name,
            'budget' : budget,
            })

    def post(self, request):
        pass



#login user
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


#Money spent CBV under
class MoneySpentView(View):
    model = Item
    template_name = "money_spent.html"
    form = ItemForm
    
    def get(self, request):
        items = Item.objects.all()
        filter = ItemFilter(request.GET, queryset=items)
        items = filter.qs
        sum_price = sum(item.price for item in items)
        context = {'items': items, 'filter': filter, 'sum_price':sum_price}
        return render(request, self.template_name, context)

    def post(self, request): 
        name = request.POST['item_name']
        description = request.POST['description']
        time_it_was_bought = datetime.now()
        price = request.POST['price']
        user = request.user
        item = Item.objects.create(name=name, description=description, time_it_was_bought=time_it_was_bought, price=price, user=user)
        item.save()
        return HttpResponseRedirect(self.request.path_info)

class ItemDetailView(DetailView):
    model = Item
    template_name = "detail.html"

    def get_object(self):
        _id = self.kwargs.get("id")
        return get_object_or_404(self.model, id=_id)

def delete_item(request, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()
    return redirect('money_spent')

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
            return render(request, 'index.html')      
    else:  
        form = UserCreationForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'register.html', context)


class ProfileView(TemplateView):
    template_name = "profile.html"

class ProfileUpdateView(UpdateView):
    template_name = "profile_update.html"
    form_class = UserUpdateForm
    model = User
    success_url = "/users/profile"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

#Standing order CBV under
class StandingOrderView(CreateView):
    template_name = "standing_orders.html"
    model = StandingOrder
    form_type = StandingOrderForm

    def get(self, request):
        standing_orders = self.model.objects.all()
        form = self.form_type
        context = {'standing_order': standing_orders, 'form': form }
        return render(request, self.template_name, context)


    def post(self, request):
        form = self.form_type(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('standing_order')
        else:
            return redirect('standing_order')

class StandingOrderUpdateView(UpdateView):
    model = StandingOrder
    query_set = model.objects.all()
    template_name = "standing_order_update.html"
    form_class = StandingOrderForm
    success_url = "/users/standing_orders"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class StandingOrderDeleteView(DeleteView):
    model = StandingOrder
    template_name = "standing_order_delete.html"
    success_url = "/users/standing_orders"
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)






