from django.db import models

class Nastamba(models.Model):
    class Meta:
        verbose_name = "Nastamba"
        verbose_name_plural = "Nastambe"

    BROJ_CHOICES = [
        ('Mračna', 'Mračna'),
        ('Grijana', 'Grijana'),
        ('Osunčana', 'Osunčana'),
    ]
    
    id = models.AutoField(primary_key=True)
    vrsta = models.CharField(max_length=50, choices=BROJ_CHOICES)
    ime = models.CharField(max_length=100, blank=True, null=True)  # Opcionalno
    centralna_tocka_lat = models.FloatField()  # Latitude kao decimalna vrijednost
    centralna_tocka_lng = models.FloatField()  # Longitude kao decimalna vrijednost
    opis = models.TextField(blank=True, null=True)  # Možeš koristiti opisni tekst umjesto geometrije
    biljke = models.TextField(blank=True, null=True)
    stabla = models.TextField(blank=True, null=True)
    sekundarne_zivotinje = models.TextField(blank=True, null=True)
    evidencija_prisutnosti = models.BooleanField(default=False)  # Prisutnost slučajno/namjerno
    
    # Soft delete polje za arhiviranje
    je_aktivna = models.BooleanField(default=True)

    def __str__(self):
        return self.ime or f'Nastamba {self.broj}'
    
class Zivotinja(models.Model):
    class Meta:
        verbose_name = "Zivotinja"
        verbose_name_plural = "Zivotinje"

    hrvatski_naziv = models.CharField(max_length=255)
    latinski_naziv = models.CharField(max_length=255)
    engleski_naziv = models.CharField(max_length=255)
    ime = models.CharField(max_length=255, blank=True, null=True)
    broj = models.IntegerField(blank=True, null=True)  # for group animals
    nastamba = models.ForeignKey(Nastamba, on_delete=models.SET_NULL, null=True)
    porijeklo = models.CharField(max_length=50, choices=[
        ('Kupovina', 'Kupovina'),
        ('Donacija', 'Donacija'),
        ('Rođenje', 'Rođenje'),
    ])
    datum_nastanka = models.DateField()
    arhiviran = models.BooleanField(default=False)  # for archived animals (dead)

    def __str__(self):
        return self.ime or self.hrvatski_naziv
    
class Obaveza(models.Model):
    class Meta:
        verbose_name = "Obaveza"
        verbose_name_plural = "Obveze"
        
    zivotinja = models.ForeignKey(Zivotinja, on_delete=models.CASCADE)
    vrsta_obaveze = models.CharField(max_length=255)  # e.g., feeding, cleaning
    status = models.CharField(max_length=10, choices=[
        ('Obavljeno', 'Obavljeno'),
        ('Zakazano', 'Zakazano'),
    ])
    datum = models.DateField()
    komentari = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.vrsta_obaveze} - {self.zivotinja}'
    
class Radnik(models.Model):
    class Meta:
        verbose_name = "Radnik"
        verbose_name_plural = "Radnici"

    ime = models.CharField(max_length=255)
    prezime = models.CharField(max_length=255)
    kontakt = models.CharField(max_length=255)
    obrazovanje = models.CharField(max_length=255)
    sposobnost = models.CharField(max_length=255)
    rok_trajanja_kvalifikacija = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.ime} {self.prezime}'
    
class KalendarRada(models.Model):
    class Meta:
        verbose_name_plural = "Kalendar rada"

    radnik = models.ForeignKey(Radnik, on_delete=models.CASCADE)
    datum = models.DateField()
    dostupnost = models.CharField(max_length=15, choices=[
        ('Dostupan', 'Dostupan'),
        ('Na odmoru', 'Na odmoru'),
        ('Bolovanje', 'Bolovanje'),
    ])

    def __str__(self):
        return f'{self.radnik} - {self.datum} - {self.dostupnost}'
    
class Trosak(models.Model):
    class Meta:
        verbose_name = "Trosak"
        verbose_name_plural = "Troskovi"

    zivotinja = models.ForeignKey(Zivotinja, on_delete=models.CASCADE)
    opis = models.CharField(max_length=255)
    kolicina = models.DecimalField(max_digits=10, decimal_places=2)
    datum = models.DateField()

    def __str__(self):
        return f'{self.opis} - {self.zivotinja}'
    
class GrupnaPosjeta(models.Model):
    class Meta:
        verbose_name = "Grupna posjeta"
        verbose_name_plural = "Grupne posjete"

    datum = models.DateField()
    vodic = models.ForeignKey(Radnik, on_delete=models.SET_NULL, null=True)
    broj_posjetitelja = models.IntegerField()

    def __str__(self):
        return f'Posjeta na datum {self.datum} - {self.vodic}'

class Nezgoda(models.Model):
    class Meta:
        verbose_name = "Nezgoda"
        verbose_name_plural = "Nezgode"

    vrsta = models.CharField(max_length=255)
    utjecaj = models.TextField()
    nastamba = models.ForeignKey(Nastamba, on_delete=models.CASCADE)
    zivotinja = models.ForeignKey(Zivotinja, on_delete=models.CASCADE)
    komentari = models.TextField(blank=True, null=True)
    trosak_sanacije = models.DecimalField(max_digits=10, decimal_places=2)
    datum = models.DateField()

    def __str__(self):
        return f'Nezgoda - {self.vrsta} - {self.datum}'