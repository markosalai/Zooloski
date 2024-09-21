from django import forms
from .models import Nastamba, Zivotinja, Radnik, Obaveza, Nezgoda, Trosak

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
class ObavezaForm(forms.ModelForm):
    class Meta:
        model = Obaveza
        fields = ['zivotinja', 'vrsta_obaveze', 'status', 'datum', 'komentari']
class NezgodaForm(forms.ModelForm):
    class Meta:
        model = Nezgoda
        fields = ['vrsta', 'utjecaj', 'nastamba', 'zivotinja', 'komentari','trosak_sanacije','datum']
class TrosakForm(forms.ModelForm):
    class Meta:
        model = Trosak
        fields = ['zivotinja', 'opis', 'kolicina', 'datum']

