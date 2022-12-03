
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from .models import *
from datetime import date, datetime
from .filters import ItemFilter
from django.views.generic import *
from .forms import ItemForm
from reportlab.pdfgen import canvas
import io
from .services import *

# Create your views here.
class IndexView(View):
    model = Profile

    def get(self, request):
        user = request.user
        if not user: 
            return redirect('login')
        else:
            name = user.username
            items = Item.objects.filter(user=request.user)
            standing_orders = StandingOrder.objects.filter(user = request.user)
            sum_items_price = get_sum_items(request.user, datetime.now().month)
            sum_orders_price = get_sum_orders(request.user)
            remaining_budget = get_budget(request.user, datetime.now().month)
            return render(request, "index.html", {
            'standing_orders': standing_orders,
            'items' : items,
            'name' : name,  
            'sum_items': sum_items_price,
            'sum_orders' : sum_orders_price,
            'remaining_budget' : remaining_budget,
            })

    def post(self, request):
        pass



#login user
class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You have successfully logged in {username}")
            return redirect('index')
        else:
            messages.success(request, f"Logging in failed try again.")
            return redirect('login')
        
    def get(self, request):
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, f'You have successfully logged out.')
        return redirect('login')



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
        return redirect('money_spent')

class ItemDetailView(DetailView):
    model = Item
    template_name = "detail.html"

    def get_object(self):
        _id = self.kwargs.get("id")
        return get_object_or_404(self.model, id=_id)

class ItemDeleteView(DeleteView):
    model = Item
    def get(self, request, item_id):
        item = self.model.objects.get(id = item_id)
        item.delete()
        return redirect('money_spent')

class RegisterView(View):
    template_name = "register.html"

    def post(self, request):
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
            messages.success(request, "Something went wrong")
            return self.get(request)
    
    def get(self, request):
        form = UserCreationForm()
        context = {
            'form' : form, 
        }
        return render(request, self.template_name, context=context)
        
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


class UserAccountInformationUpdateView(UpdateView):
    template_name = "user_update.html"
    model = Profile 
    form_class = UserAccountUpdateForm
    success_url = "/users/account_information"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)

#Standing order CBV under
class StandingOrderView(CreateView):
    template_name = "standing_orders.html"
    model = StandingOrder
    form_type = StandingOrderForm

    def get(self, request):
        standing_orders = self.model.objects.filter(user = request.user)
        form = self.form_type
        context = {
            'standing_order': standing_orders, 
            'form': form 
        }
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


class ReportGenerationView(View):
    template_name = "reports.html"
    
    def get(self, request):
        user = request.user
        this_month = get_month()
        monthly_income = user.profile.monthly_income
        context = {'user': user, 'this_month' : this_month, 'monthly_income': monthly_income}
        return render(request, self.template_name, context=context)

    def post(self, request):
        user = request.user
        buffer = io.BytesIO()
        this_month = get_month()
        p = canvas.Canvas(buffer)
        string = f"Report for {this_month}"
        sum_items = f"Items summary: {user.profile.sum_items} CZK"
        sum_orders = f"Orders summary: {user.profile.sum_orders} CZK"
        monthly_income = f"Monthly_income: {user.profile.monthly_income}"
        budget = f"Budget: {user.profile.calculate_budget} CZK"
        p.drawString(50, 780, string)
        p.drawString(60, 760, monthly_income)
        p.drawString(60, 740, sum_items)
        p.drawString(60, 720, sum_orders)
        p.drawString(60, 700, budget)
        p.showPage()
        p.save()

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename="report.pdf")