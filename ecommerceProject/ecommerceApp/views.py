from django.shortcuts import redirect, render
from django.contrib import messages
from ecommerceApp.models import *

def index(request):
    return render(request, 'index.html')

def men(request):
    return render(request, 'men.html')

def women(request):
    return render(request, 'women.html')


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

    return render(request, 'admin_dash.html')
