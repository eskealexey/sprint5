"""
Views
"""
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Advertisement, Statistic


def logout_view(request):
    """
    Logout view
    """
    logout(request)
    return redirect('home')

from django.shortcuts import render, redirect
from .forms import SignUpForm, AdvertisementForm
from django.contrib.auth import login


def signup(request):
    """
    Signup view
    """
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
    """
    Home view
    """
    return render(request, 'home.html')


def advertisement_list(request):
    """
    Advertisement list view
    """
    advertisements = Advertisement.objects.all()

    paginator = Paginator(advertisements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, 'board/advertisement_list.html', {'advertisements': page_obj})


def advertisement_detail(request, pk):
    """
    Advertisement detail view
    """
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


def advertisement_remove(request, pk):
    """
    Remove advertisement view
    """
    if request.method == "POST":
        advertisement = Advertisement.objects.get(pk=pk)
        advertisement.delete()
        return redirect('board:advertisement_list')
    else:
        return redirect('board:advertisement_list')


@login_required
def add_advertisement(request):
    """
    Add advertisement view
    """
    if request.method == "POST":
        form = AdvertisementForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            request.user.save()

            statistic = Statistic.objects.filter(author=request.user)
            if not statistic:
                Statistic.objects.create(author=request.user, ad_count=1)
            else:
                statistic = Statistic.objects.all().filter(author=request.user)
                for stat in statistic:
                    print(stat.ad_count)
                    stat.ad_count += 1
                    stat.save()

            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    """
    Edit advertisement view
    """
    advertisement_ = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST or None, request.FILES or None, instance=advertisement_)
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
    """
    Удаление объявления с подтверждением
    """
    if request.method == "POST":
        advertisement = Advertisement.objects.get(pk=pk)
        advertisement.delete()

        statistic = Statistic.objects.filter(author=request.user)
        if not statistic:
            pass
        else:
            statistic = Statistic.objects.all().filter(author=request.user)
            for stat in statistic:
                print(stat.ad_count)
                stat.ad_count -= 1
                stat.save()

        return redirect('board:advertisement_list')
    return render(request, 'board/advertisement_delete.html',)


def add_likes(request, pk):
    """
    Добавление лайков
    """
    like = Advertisement.objects.get(pk=pk)
    if request.method == "GET":
        like.likes += 1
        like.save()
        return redirect('board:advertisement_detail', pk=pk)
    return render(request, 'board/advertisement_detail.html')


def add_dislikes(request, pk):
    """
    Добавление дизлайков
    """

    like = Advertisement.objects.get(pk=pk)
    if request.method == "GET":
        like.dislikes += 1
        like.save()
        return redirect('board:advertisement_detail', pk=pk)
    return render(request, 'board/advertisement_detail.html')
