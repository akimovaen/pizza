from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import Menu, Items


# Create your views here.

def display_menu():
    menu_list = Menu.objects.all()
    menu = []
    for i in range(len(menu_list)):
        dishes = Items.objects.filter(menu=i+1)
        data = []
        name = menu_list[i]
        print(name)
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
        
        menu.append({'name': name.name, 'dishes': data})
    
    return menu


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "menu": display_menu()
    }

    return render(request, "orders/index.html", context)


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

