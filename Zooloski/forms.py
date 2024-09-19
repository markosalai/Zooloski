from django import forms
from .models import Nastamba, Zivotinja, Radnik

class NastambaForm(forms.ModelForm):
    class Meta:
        model = Nastamba
        fields = ['vrsta', 'ime', 'centralna_tocka_lat', 'centralna_tocka_lng', 'opis', 'biljke', 'stabla', 'sekundarne_zivotinje', 'evidencija_prisutnosti']
class ZivotinjaForm(forms.ModelForm):
    class Meta:
        model = Zivotinja
        fields = ['hrvatski_naziv', 'latinski_naziv', 'engleski_naziv', 'ime', 'broj', 'nastamba', 'porijeklo', 'datum_nastanka']
class RadnikForm(forms.ModelForm):
    class Meta:
        model = Radnik
        fields = ['ime', 'prezime', 'kontakt', 'obrazovanje', 'sposobnost', 'rok_trajanja_kvalifikacija']
