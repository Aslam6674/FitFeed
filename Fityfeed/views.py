from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import fooditemFilter


@login_required(login_url='login')
@admin_only
def home(request):
    breakfast = Category.objects.filter(name='breakfast').first()
    lunch = Category.objects.filter(name='lunch').first()
    dinner = Category.objects.filter(name='dinner').first()
    snacks = Category.objects.filter(name='snacks').first()

    breakfast_items = breakfast.fooditem_set.all()[:5] if breakfast else []
    lunch_items = lunch.fooditem_set.all()[:5] if lunch else []
    dinner_items = dinner.fooditem_set.all()[:5] if dinner else []
    snacks_items = snacks.fooditem_set.all()[:5] if snacks else []

    customers = Customer.objects.all()
    context = {
        'breakfast': breakfast_items,
        'lunch': lunch_items,
        'dinner': dinner_items,
        'snacks': snacks_items,
        'customers': customers,
    }
    return render(request, 'main.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fooditem(request):
    breakfast = Category.objects.filter(name='breakfast').first()
    lunch = Category.objects.filter(name='lunch').first()
    dinner = Category.objects.filter(name='dinner').first()
    snacks = Category.objects.filter(name='snacks').first()

    breakfast_items = breakfast.fooditem_set.all() if breakfast else []
    lunch_items = lunch.fooditem_set.all() if lunch else []
    dinner_items = dinner.fooditem_set.all() if dinner else []
    snacks_items = snacks.fooditem_set.all() if snacks else []

    context = {
        'breakfast': breakfast_items,
        'bcnt': len(breakfast_items),
        'lunch': lunch_items,
        'lcnt': len(lunch_items),
        'dinner': dinner_items,
        'dcnt': len(dinner_items),
        'snacks': snacks_items,
        'scnt': len(snacks_items),
    }
    return render(request, 'fooditem.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createfooditem(request):
    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'createfooditem.html', context)


@unauthorized_user
def registerPage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)
            email = form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=username, email=email)
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthorized_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def userPage(request):
    user = request.user
    cust = user.customer
    fooditems = Fooditem.objects.all()
    myfilter = fooditemFilter(request.GET, queryset=fooditems)
    fooditems = myfilter.qs

    total = UserFooditem.objects.all()
    myfooditems = total.filter(customer=cust)
    cnt = myfooditems.count()

    finalFoodItems = []
    for food in myfooditems:
        for food_item in food.fooditem.all():
            finalFoodItems.append(food_item)

    totalCalories = sum(f.calorie for f in finalFoodItems)
    CalorieLeft = 2000 - totalCalories

    context = {
        'CalorieLeft': CalorieLeft,
        'totalCalories': totalCalories,
        'cnt': cnt,
        'foodlist': finalFoodItems,
        'fooditem': fooditems,
        'myfilter': myfilter,
    }
    return render(request, 'user.html', context)


@login_required(login_url='login')
def addFooditem(request):
    user = request.user
    cust = user.customer
    if request.method == "POST":
        form = addUserFooditem(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userPage')
    form = addUserFooditem()
    context = {'form': form}
    return render(request, 'addUserFooditem.html', context)
