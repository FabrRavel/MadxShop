from django.shortcuts import render,redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def category(request, foo):

    foo = foo.replace('-', ' ')

    try:

        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request,("Cette catégorie n'existe pas"))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("Connexion réussie. Bienvenue"))
            return redirect('home')
        else: 
            messages.success(request,("Il y a une erreur dans le mot de passe ou  dans le nom d'utilisateur. VEUILLEZ SAISIR CORRECTEMENT VOTRE NOM ET VOTRE MOT DE PASSE!!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("Merci d'avoir utilisé Madx Shop. Vous vous êtes bien déconnectés"))
    return redirect('login')



def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Votre inscription est bien validé"))
            return redirect('home')
        else:
            messages.success(request, ("Whoops! Il y a un problème dans votre demande d'inscription"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})