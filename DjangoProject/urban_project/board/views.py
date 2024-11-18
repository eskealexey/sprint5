from django.template.context_processors import request

from .models import Advertisement

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def logout_view(request):
    '''
    Logout view
    '''
    logout(request)
    return redirect('home')

from django.shortcuts import render, redirect
from .forms import SignUpForm, AdvertisementForm
from django.contrib.auth import login


def signup(request):
    '''
    Signup view
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    '''
    Home view
    '''
    return render(request, 'home.html')

def advertisement_list(request):
    '''
    Advertisement list view
    '''
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

def advertisement_detail(request, pk):
    '''
    Advertisement detail view
    '''
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

def advertisement_remove(request, pk):
    '''
    Remove advertisement view
    '''
    if request.method == "POST":
        advertisement = Advertisement.objects.get(pk=pk)
        advertisement.delete()
        return redirect('board:advertisement_list')
    else:
        return redirect('board:advertisement_list')

@login_required
def add_advertisement(request):
    '''
    Add advertisement view
    '''
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    '''
    Edit advertisement view
    '''
    advertisement_ = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advertisement_)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm(instance=advertisement_)
    return render(request, 'board/edit_advertisement.html', {'form': form})

@login_required
def delete_advertisement(request, pk):
    '''
    Удаление объявления с подтверждением
    '''
    if request.method == "POST":
        advertisement = Advertisement.objects.get(pk=pk)
        advertisement.delete()
        return redirect('board:advertisement_list')

    return render(request, 'board/advertisement_delete.html',)