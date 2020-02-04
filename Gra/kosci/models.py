from __future__ import unicode_literals
from django.db import models


class GraModel(models.Model):
    # model dla gracza 1 i 2 baza bezsensu bo przyjmujemy że będzie posiadać 2 rekordy no ale cóż jakos trza dane tzymać
    nrGracza = models.IntegerField()  # gracz 1 id 1 gracz 2 id 2
    imie = models.CharField(max_length=55)  # niech gracz poda jako że niby taki sapekt presonalizacji
    kosc1 = models.IntegerField()
    kosc2 = models.IntegerField()
    kosc3 = models.IntegerField()
    kosc4 = models.IntegerField()
    kosc5 = models.IntegerField()
    ruch = models.IntegerField()  # jeśli oba równe (dla id 1 i 2) wtedy go jeśli jeden mniejszy to większy czeka
    wynik = models.IntegerField()  # sumaryczny wynik gracza
    nrGry = models.IntegerField()  # zliczajmy gry


class GraHistoria(models.Model):
    # dodawnae rekordy do histori (każdy ruch)
    nrHist = models.IntegerField()
    imie = models.CharField(max_length=55)
    kosc1 = models.IntegerField()
    kosc2 = models.IntegerField()
    kosc3 = models.IntegerField()
    kosc4 = models.IntegerField()
    kosc5 = models.IntegerField()
    ruch = models.IntegerField()
    wynik = models.IntegerField()
    nrGry = models.IntegerField()  # zliczajmy nr gry


class GraRanking(models.Model):
    # dodawanie rekordów na koniec gry
    nrRank = models.IntegerField()
    imie = models.CharField(max_length=55)
    wynik = models.IntegerField()
    nrGry = models.IntegerField()  # zliczajmy gry
