from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import NastambaForm
from django.contrib.auth.views import LoginView
# Create your views here.

#def pocetna(request):
 #   return render(request, 'pocetna.html')

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
