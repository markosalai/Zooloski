from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import NastambaForm, ZivotinjaForm
from django.contrib.auth.views import LoginView
# Create your views here.

def pocetna(request):
    return render(request, 'pocetna.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/zooloski/nastambe/'  # Redirect admin users to nastambe page
        else:
            return '/'  # Regular users can be redirected elsewhere (home page or any other page)
        
# Prikaz svih nastambi
def nastamba_list(request):
    nastambe = Nastamba.objects.filter(je_aktivna=True)  # Prikaz samo aktivnih nastambi
    return render(request, 'nastamba_list.html', {'nastambe': nastambe})

# Detaljan prikaz nastambe
def nastamba_detail(request, id):
    nastamba = get_object_or_404(Nastamba, id=id, je_aktivna=True)
    return render(request, 'nastamba_detail.html', {'nastamba': nastamba})

# Kreiranje nove nastambe
def nastamba_create(request):
    if request.method == 'POST':
        form = NastambaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nastamba_list')
    else:
        form = NastambaForm()
    return render(request, 'nastamba_form.html', {'form': form})

# Uređivanje postojeće nastambe
def nastamba_update(request, id):
    nastamba = get_object_or_404(Nastamba, id=id)
    if request.method == 'POST':
        form = NastambaForm(request.POST, instance=nastamba)
        if form.is_valid():
            form.save()
            return redirect('nastamba_list')
    else:
        form = NastambaForm(instance=nastamba)
    return render(request, 'nastamba_form.html', {'form': form})

# Arhiviranje nastambe (soft delete)
def nastamba_archive(request, id):
    nastamba = get_object_or_404(Nastamba, id=id)
    nastamba.je_aktivna = False  # Soft delete, postavljanje je_aktivna na False
    nastamba.save()
    return redirect('nastamba_list')

def zivotinja_list(request):
    zivotinje = Zivotinja.objects.filter(arhiviran=False)  # Prikazuje samo aktivne životinje
    if request.method == "POST":
        form = ZivotinjaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zivotinja_list')
    else:
        form = ZivotinjaForm()
    return render(request, 'zivotinja_list.html', {'zivotinje': zivotinje, 'form': form})

def zivotinja_create(request):
    if request.method == 'POST':
        form = ZivotinjaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zivotinja_list')
    else:
        form = ZivotinjaForm()
    return render(request, 'zivotinja_form.html', {'form': form})

def zivotinja_update(request, id):
    zivotinja = get_object_or_404(Zivotinja, id=id)  # Dohvati životinju ili prikaži grešku 404
    if request.method == 'POST':
        form = ZivotinjaForm(request.POST, instance=zivotinja)
        if form.is_valid():
            form.save()
            return redirect('zivotinja_list')  # Nakon uređivanja, preusmjeri nazad na listu životinja
    else:
        form = ZivotinjaForm(instance=zivotinja)
    return render(request, 'zivotinja_form.html', {'form': form})