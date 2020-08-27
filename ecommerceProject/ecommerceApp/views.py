from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from ecommerceApp.models import *

def index(request):
    context = {}
    if 'user_id' in request.session:
        context['user'] = User.objects.get(id=request.session['user_id'])

    if 'cart' in request.session:
        context['cart_item_count'] = sum(request.session['cart'].values())
    else:
        context['cart_item_count'] = 0

    return render(request, 'index.html', context)


def men(request):
    return render(request, 'men.html')

def women(request):
    context = {
        'all_products': Item.objects.all().exclude(category="men"),
    }

    if 'user_id' in request.session:
        context['user'] = User.objects.get(id=request.session['user_id'])

    if 'cart' in request.session:
        context['cart_item_count'] = sum(request.session['cart'].values())
    else:
        context['cart_item_count'] = 0

    return render(request, 'women.html',context)


def admin(request):
    if 'admin_email' in request.session:
        return redirect('/admin/dashboard')

    return render(request, 'admin_login.html')


def admin_login(request):
    if request.method == 'POST':
        errors = Admin.objects.admin_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print()
                messages.error(request, value)

        else:
            request.session['admin_email'] = request.POST['login_email']
            print('login success')
            return redirect('/admin/dashboard')

    return redirect('/admin')


def admin_logout(request):
    request.session.flush()
    return redirect('/admin')


def admin_dash(request):
    if 'admin_email' not in request.session:
        return redirect('/admin')

    context = {
        'all_products': Item.objects.all(),
    }

    return render(request, 'admin_dash.html', context)


def add_product(request):
    if request.method == 'POST':
        Item.objects.create(
            category = request.POST['category'],
            name = request.POST['product_name'],
            price = request.POST['price'],
            front_pic = request.POST['front_pic'],
            back_pic = request.POST['back_pic'],
            desc = request.POST['desc']
        )

    return redirect('/admin/dashboard')


def carts(request):
   
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session["user_id"])
    }
    return render(request, 'carts.html', context)



def register(request):
    return render(request, 'register.html')

def user_create(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns,
        )     
        request.session['user_id'] = user.id
        return redirect('/carts')
        


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        user_to_login = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login.id 
        return redirect('/carts')

def logout(request):
    request.session.flush()
    return redirect('/')

def details(request, product_id):
    item = Item.objects.get(id=product_id)
    return JsonResponse(
        {
            "name": item.name, 
            "price": item.price, 
            "desc": item.desc,
            "image":item.front_pic
        })