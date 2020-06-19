import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


from .models import *


# Create your views here.

def display_menu():
    menu_list = Menu.objects.all()
    menu = []
    for i in range(len(menu_list)):
        dishes = Items.objects.filter(menu=i+1)
        data = []
        name = menu_list[i]
        for dish in dishes:
            if dish.trait:
                item = {'name': dish.name, dish.trait: dish.price}
            elif dish.price:
                item = {'name': dish.name, 'price': dish.price}
            else:
                item = {'name': dish.name}
            
            index = -1

            for i in range(len(data)):
                if dish.name == data[i]['name']:
                    index = i
            
            if index == -1:
                data.append(item)
            else:
                data[index][dish.trait] = dish.price
        
        menu.append({'name': name.name, 'image': name.image, 'dishes': data})
    
    return menu


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "menu": display_menu()
    }
    user_shop_cart = ShopCart.objects.filter(user__username=request.user).all()
    if user_shop_cart:
        shop_cart = []
        for dish in user_shop_cart:
            dish_cart = ShopCart.objects.get(id=dish.id)
            shop_cart.append(dish_cart.cart_view())
        context["user_shop_cart"] = shop_cart
        print(shop_cart)

    return render(request, "orders/index.html", context)


def get_additions(data, menu):
    list_add = []
    for item in data:
        name = item.replace('&amp;', '&')    
        add = Items.objects.get(menu__name=menu, name=name)
        list_add.append(add)

    return list_add


@csrf_exempt
def shopping_cart(request):
    username = request.POST.get("user")
    menu = request.POST.get("menu")
    dish = request.POST.get("name")
    name = dish.replace('&amp;', '&')
    size = request.POST.get("size")
    data_toppings = json.loads(request.POST.get("toppings"))
    data_additions = json.loads(request.POST.get("additions"))
    list_top = []
    add1 = None
    add2 = None
    add3 = None

    if data_toppings['data']:
        list_top = get_additions(data_toppings['data'], "Toppings")
    elif data_additions['data']:
        list_top = get_additions(data_additions['data'], "Subs")

    user = User.objects.get(username=username)
    
    if size:
        dish = Items.objects.get(menu__name=menu, name=name, trait=size)
    else:
        dish = Items.objects.get(menu__name=menu, name=name)
    
    if len(list_top) == 1:
        add1 = list_top[0]
    elif len(list_top) == 2:
        add1 = list_top[0]
        add2 = list_top[1]
    elif len(list_top) == 3:
        add1 = list_top[0]
        add2 = list_top[1]
        add3 = list_top[2]
    
    cart = ShopCart(
        user = user,
        dish = dish,
        add1 = add1,
        add2 = add2,
        add3 = add3)
    cart.save()
    
    return JsonResponse({"shop_cart": cart.cart_view()})


@csrf_exempt
def delete_dish(request):
    dish_id = request.POST.get("id")
    try:
        dish = ShopCart.objects.get(pk=dish_id)
    except ObjectDoesNotExist:
        return JsonResponse({"success": "false"})
    
    dish.delete()
    return JsonResponse({"success": "true"})


# @csrf_exempt
# def place_order(request):
#     data_id = json.loads(request.POST.get("id"))
#     print(data_id)
#     for i in data_id['id']:
#         try:
#             dish = ShopCart.objects.get(pk=i)
#         except ObjectDoesNotExist:
#             return JsonResponse({"success": "false"})
    
        
#         dish.delete()
    
#     return JsonResponse({"success": "true"})


def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = None
    if username and password:
        user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = None
        if username and email and password:
            user = User.objects.create_user(username, email, password)
    else:
        return render(request, "orders/register.html")

    if user is not None:
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/register.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

