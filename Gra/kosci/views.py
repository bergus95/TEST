import random
from Gra.kosci.liczenie import obliczWynik
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import request
from django.template.defaulttags import regroup
from django.template import loader

from Gra.kosci.form import UsernameForm
from Gra.kosci.models import GraModel, GraHistoria, GraRanking

import socket
import select
import errno
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# REQUEST COMMANDS
ASK_FOR_SIT = "ask-for-sit"
UPDATE_POINTS = "update-points"
FREE_SIT = "free-sit"

G1_LABEL = "G1"
G2_LABEL = "G2"

PIERWSZE_LOSOWANIE = True


def start(request):
    print(request)
    if request.method == 'POST' and 'ranking' in request.POST:
        return HttpResponseRedirect('/ranking/')
    elif request.method == 'POST' and 'historia' in request.POST:

        return HttpResponseRedirect('/historia/')

    elif request.method == 'POST' and 'clear' in request.POST:

        GraRanking.objects.all().delete()
        # GraRanking.save()
        GraHistoria.objects.all().delete()
        # GraHistoria.save()
        return render(request, 'kosci/start.html')
    elif request.method == 'POST' and 'cleargamers' in request.POST:

        GraModel.objects.all().delete()
        return render(request, 'kosci/start.html')

    elif request.method == 'POST' and 'nowagra' in request.POST:
        return HttpResponseRedirect('/wybor/')
    else:
        return render(request, 'kosci/start.html')


def wybor(request):
    form = UsernameForm(request.POST)

    if request.method == 'POST' and 'gracz1' in request.POST:  # -------------------------------------- WYBÓR GRACZ 1
        if form.is_valid():
            username = form['username'].value()
            request.session['username'] = username
            request.session['playerID'] = 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = ASK_FOR_SIT + ":" + G1_LABEL + ":" + username
            s.sendall(bytes(message.encode('utf-8')))
            data = s.recv(1024)
            print('&&&&&&&&&')
            print(data.decode('utf-8'))
            print('&&&&&&&&&')
            message = data.decode('utf-8')
            print('Received ', message)
            if int(message) == 1:
                s.close()
                global PIERWSZE_LOSOWANIE
                PIERWSZE_LOSOWANIE = True
                request.session['move'] = 0
                return HttpResponseRedirect('/gra/')
            else:
                s.close()
                return HttpResponseRedirect('/zajete/')

    elif request.method == 'POST' and 'gracz2' in request.POST:  # -------------------------------------- WYBÓR GRACZ 2
        if form.is_valid():
            username = form['username'].value()
            request.session['username'] = username
            request.session['playerID'] = 2

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = ASK_FOR_SIT + ":" + G2_LABEL + ":" + username
            s.sendall(bytes(message.encode('utf-8')))
            data = s.recv(1024)
            message = data.decode('utf-8')
            print('Received ', message)
            if int(message) == 1:
                s.close()
                request.session['move'] = 0
                return HttpResponseRedirect('/gra/')
            else:
                s.close()
                return HttpResponseRedirect('/zajete/')

    elif request.method == 'POST' and 'cleargamers' in request.POST:
        GraModel.objects.all().delete()
        return render(request, 'kosci/wyborgracza.html')

    elif request.method == 'POST' and 'start' in request.POST:
        return HttpResponseRedirect('/')
    else:
        template = loader.get_template('kosci/wyborgracza.html')
        context = {
            'form': form,
        }
        # return render(request, 'kosci/wyborgracza.html')
        return HttpResponse(template.render(context, request))


def zajete(request):
    return render(request, 'kosci/zajete.html')


def historia(request):
    if request.method == 'POST' and 'start' in request.POST:
        return HttpResponseRedirect('/')
    else:
        hist = GraHistoria.objects.all()
        print("\n\nhistoria\n", hist)
        return render(request, 'kosci/historia.html', {'hist': hist})


def ranking(request):
    if request.method == 'POST' and 'start' in request.POST:
        return HttpResponseRedirect('/')
    else:
        rank = GraRanking.objects.all()
        print("\n\nRanking\n\n", rank)
        return render(request, 'kosci/ranking.html', {'rank': rank})


def koniec(request):
    template = loader.get_template('kosci/koniec.html')
    context = {
        'hello': 'Koniec gry',
    }
    return HttpResponse(template.render(context, request))


firstg1 = True


def gra(request):  # ========================================================================================== GRA
    nickname = request.session.get('username')
    print("nick: ", request.session.get('username'))
    template = loader.get_template('kosci/gra.html')

    kosci_obecne = request.session.get('kosci')
    zaznaczone_kosci = request.POST.getlist('check')

    global PIERWSZE_LOSOWANIE

    if PIERWSZE_LOSOWANIE:
        kosci = [random.randrange(1, 6, 1) for kosc in range(1, 6)]
        request.session['kosci'] = kosci
        PIERWSZE_LOSOWANIE = False
    else:
        kosci = kosci_obecne
        if not 'kosc1' in zaznaczone_kosci:
            kosci[0] = random.randrange(1, 6, 1)
        else:
            kosci[0] = kosci_obecne[0]
        if not 'kosc2' in zaznaczone_kosci:
            kosci[1] = random.randrange(1, 6, 1)
        else:
            kosci[1] = kosci_obecne[1]
        if not 'kosc3' in zaznaczone_kosci:
            kosci[2] = random.randrange(1, 6, 1)
        else:
            kosci[2] = kosci_obecne[2]
        if not 'kosc4' in zaznaczone_kosci:
            kosci[3] = random.randrange(1, 6, 1)
        else:
            kosci[3] = kosci_obecne[3]
        if not 'kosc5' in zaznaczone_kosci:
            kosci[4] = random.randrange(1, 6, 1)
        else:
            kosci[4] = kosci_obecne[4]

    # numer ruchu
    if request.session.get('move') is not None:
        request.session['move'] += 1
    else:
        request.session['move'] = 0

    print("kosci: ", request.session.get('kosci'))
    print(request.session.get('move'))
    context = {
        'kosci': kosci,
        'dozwolony_ruch': request.session.get('move') % 3,
    }

    if not request.session.get('move') % 3:
        wynik = obliczWynik(kosci[0], kosci[1], kosci[2], kosci[3], kosci[4])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = UPDATE_POINTS + ":" + nickname + ":" + str(wynik)
            s.sendall(bytes(message.encode('utf-8')))

    return HttpResponse(template.render(context, request))


def gracz1(request):
    print('###########################')
    print(request)
    print('###########################')
    global firstg1
    if request.method == 'POST' and 'start' in request.POST:
        firstg1 = True
        # gracz1 = GraModel.objects.filter(nrGracza = 0)
        # gracz1[0].ruch = 0
        # gracz1[0].save()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = FREE_SIT + ":" + G1_LABEL
            # print(message)
            s.sendall(bytes(message.encode('utf-8')))
        return HttpResponseRedirect('/')
    else:
        some_var = request.POST.getlist('check')
        # print("\n\n\n\n\n",some_var,"\n\n\n\n\n")
        gracz1 = GraModel.objects.filter(nrGracza=0)
        # print("\n\n___GRACZ1__\n\n", gracz1)
        # print("\n\n___GRACZ1__\n\n", gracz1[0].ruch)
        if not gracz1:
            # kiedy nie ma obiektu
            a = GraModel(nrGracza=0, imie="gracz1", kosc1=0, kosc2=0, kosc3=0, kosc4=0, kosc5=0, ruch=0, nrGry=0,
                         wynik=0)
            print(a)
            a.save()

        # gracz1 = GraModel.objects.filter(nrGracza=0)
        gracz2 = GraModel.objects.filter(nrGracza=1)
        if firstg1:
            if not gracz1:
                gracz1 = GraModel.objects.filter(nrGracza=0)
            # kiedy pierwszy raz grasz (zaczynasz runde)
            gracz1[0].imie = "gracz1"
            if not 'kosc1' in some_var:  # y eify w stym przypadku są bez sensu ale niech zostana a moze się przydadzą
                gracz1[0].kosc1 = random.randrange(1, 6, 1)
            if not 'kosc2' in some_var:
                gracz1[0].kosc2 = random.randrange(1, 6, 1)
            if not 'kosc3' in some_var:
                gracz1[0].kosc3 = random.randrange(1, 6, 1)
            if not 'kosc4' in some_var:
                gracz1[0].kosc4 = random.randrange(1, 6, 1)
            if not 'kosc5' in some_var:
                gracz1[0].kosc5 = random.randrange(1, 6, 1)
            # print(gracz1[0].ruch)
            gracz1[0].ruch = 1
            gracz1[0].nrGry += 1
            gracz1[0].wynik = 0

            gracz1[0].save()
            firstg1 = False
        elif gracz1[0].ruch == 10:
            if gracz2:
                if gracz2[0].ruch == 10:
                    if gracz1[0].wynik > gracz2[0].wynik:
                        r = GraRanking(nrRank=GraRanking.objects.all().count() + 1, imie=gracz1[0].imie,
                                       nrGry=gracz1[0].nrGry, wynik=gracz1[0].wynik)
                        print("\n\n Ranking G1 ADD", r.nrRank, r.imie, r.wynik, r.nrGry, "\n\n\n")
                        r.save()
                        return HttpResponseRedirect('/koniec/')
                    if gracz1[0].wynik < gracz2[0].wynik:
                        return HttpResponseRedirect('/koniec/')
                    if gracz1[0].wynik == gracz2[0].wynik:
                        return HttpResponseRedirect('/koniec/')
            else:
                print("czekaj")
        elif gracz1[0].ruch % 2 == 0:
            if gracz2:
                if gracz2[0].ruch >= gracz1[0].ruch:
                    #  kiedy juz wykonał ruch i gracz2 też
                    gracz1[0].imie = "gracz1"
                    gracz1[0].kosc1 = random.randrange(1, 6, 1)
                    gracz1[0].kosc2 = random.randrange(1, 6, 1)
                    gracz1[0].kosc3 = random.randrange(1, 6, 1)
                    gracz1[0].kosc4 = random.randrange(1, 6, 1)
                    gracz1[0].kosc5 = random.randrange(1, 6, 1)
                    gracz1[0].ruch += 1
                    gracz1[0].wynik = gracz1[0].wynik
                    gracz1[0].save()
        else:
            if gracz2:
                if gracz2[0].ruch >= gracz1[0].ruch:
                    #  kiedy juz wykonał ruch i gracz2 też
                    gracz1[0].imie = "gracz1"
                    if not 'kosc1' in some_var:
                        gracz1[0].kosc1 = random.randrange(1, 6, 1)
                    if not 'kosc2' in some_var:
                        gracz1[0].kosc2 = random.randrange(1, 6, 1)
                    if not 'kosc3' in some_var:
                        gracz1[0].kosc3 = random.randrange(1, 6, 1)
                    if not 'kosc4' in some_var:
                        gracz1[0].kosc4 = random.randrange(1, 6, 1)
                    if not 'kosc5' in some_var:
                        gracz1[0].kosc5 = random.randrange(1, 6, 1)
                    gracz1[0].ruch += 1
                    print(gracz1[0].ruch % 2)
                    print("\nwynik g1: ", gracz1[0].wynik)
                    if gracz1[0].ruch % 2 == 0:  # już po inkrementacji czyli mozna zliczyć wynik rundy
                        gracz1[0].wynik += obliczWynik(gracz1[0].kosc1, gracz1[0].kosc1, gracz1[0].kosc3,
                                                       gracz1[0].kosc4, gracz1[0].kosc5)

                    print("\nwynik g1: ", gracz1[0].wynik)
                    gracz1[0].save()
        h = GraHistoria(nrHist=GraHistoria.objects.all().count() + 1, imie=gracz1[0].imie, kosc1=gracz1[0].kosc1,
                        kosc2=gracz1[0].kosc2, kosc3=gracz1[0].kosc3, kosc4=gracz1[0].kosc4, kosc5=gracz1[0].kosc5,
                        ruch=gracz1[0].ruch, nrGry=gracz1[0].nrGry, wynik=gracz1[0].wynik)
        print("\n\n HIST G1 ADD", h.nrHist, h.imie, h.ruch, h.wynik, h.nrGry, "\n\n\n")
        h.save()
        if gracz2:
            return render(request, 'kosci/gracz1.html',
                          {'kosc1': gracz1[0].kosc1, 'kosc2': gracz1[0].kosc2, 'kosc3': gracz1[0].kosc3,
                           'kosc4': gracz1[0].kosc4, 'kosc5': gracz1[0].kosc5, 'ruchg1': gracz1[0].ruch,
                           'ruchg2': gracz2[0].ruch, 'wynikg1': gracz1[0].wynik, 'wynikg2': gracz2[0].wynik})
        else:
            return render(request, 'kosci/gracz1.html',
                          {'kosc1': gracz1[0].kosc1, 'kosc2': gracz1[0].kosc2, 'kosc3': gracz1[0].kosc3,
                           'kosc4': gracz1[0].kosc4, 'kosc5': gracz1[0].kosc5, 'ruchg1': gracz1[0].ruch,
                           'ruchg2': "", 'wynikg1': gracz1[0].wynik, 'wynikg2': ""})


firstg2 = True


def gracz2(request):
    global firstg2
    if request.method == 'POST' and 'start' in request.POST:
        firstg2 = True
        # gracz2 = GraModel.objects.filter(nrGracza = 1)
        # print("\n\nruch g2 \n\n",gracz2[0].ruch)
        # gracz2[0].ruch = 0
        # print("\n\nruch g2 \n\n", gracz2[0].ruch)
        # setattr(gracz2[0], 'ruch', 0)
        # gracz2[0].save()
        # gracz2 = GraModel.objects.filter(nrGracza = 1)
        # print("\n\nruch g2 \n\n",gracz2[0].ruch)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = FREE_SIT + ":" + G2_LABEL
            # print(message)
            s.sendall(bytes(message.encode('utf-8')))
        return HttpResponseRedirect('/')
    else:
        some_var = request.POST.getlist('check')
        gracz2 = GraModel.objects.filter(nrGracza=1)
        print("\n\n___GRACZ2__\n\n", gracz2)
        # print("\n\n___GRACZ2__\n\n", gracz2[0].ruch)

        if not gracz2:
            # kiedy nie ma obiektu
            a = GraModel(nrGracza=1, imie="gracz2", kosc1=0, kosc2=0, kosc3=0, kosc4=0, kosc5=0, ruch=0, nrGry=0,
                         wynik=0)
            a.save()
        # gracz2 = GraModel.objects.filter(nrGracza=1)

        gracz1 = GraModel.objects.filter(nrGracza=0)
        if firstg2:
            if not gracz2:
                gracz2 = GraModel.objects.filter(nrGracza=1)
            # kiedy pierwszy raz grasz (zaczynasz runde)
            gracz2[0].imie = "gracz2"
            if not 'kosc1' in some_var:
                gracz2[0].kosc1 = random.randrange(1, 6, 1)
            if not 'kosc2' in some_var:
                gracz2[0].kosc2 = random.randrange(1, 6, 1)
            if not 'kosc3' in some_var:
                gracz2[0].kosc3 = random.randrange(1, 6, 1)
            if not 'kosc4' in some_var:
                gracz2[0].kosc4 = random.randrange(1, 6, 1)
            if not 'kosc5' in some_var:
                gracz2[0].kosc5 = random.randrange(1, 6, 1)
            gracz2[0].ruch = 1
            gracz2[0].nrGry += 1
            gracz2[0].wynik = 0
            gracz2[0].save()
            firstg2 = False
        elif gracz2[0].ruch == 10:
            if gracz1:
                if gracz1[0].ruch == 10:
                    if gracz1[0].wynik < gracz2[0].wynik:
                        r = GraRanking(nrRank=GraRanking.objects.all().count() + 1, imie=gracz2[0].imie,
                                       nrGry=gracz2[0].nrGry, wynik=gracz2[0].wynik)
                        print("\n\n Ranking G2 ADD", r.nrRank, r.imie, r.wynik, r.nrGry, "\n\n\n")
                        r.save()
                        return HttpResponseRedirect('/koniec/')
                    if gracz1[0].wynik > gracz2[0].wynik:
                        return HttpResponseRedirect('/koniec/')
                    if gracz1[0].wynik == gracz2[0].wynik:
                        return HttpResponseRedirect('/koniec/')
            else:
                print("czekaj")
        elif gracz2[0].ruch % 2 == 0:  # jeśli wykonał dwa rzuty to
            if gracz1:
                if gracz1[0].ruch >= gracz2[0].ruch:
                    #  kiedy juz wykonał ruch i gracz2 też
                    gracz2[0].imie = "gracz2"
                    gracz2[0].kosc1 = random.randrange(1, 6, 1)
                    gracz2[0].kosc2 = random.randrange(1, 6, 1)
                    gracz2[0].kosc3 = random.randrange(1, 6, 1)
                    gracz2[0].kosc4 = random.randrange(1, 6, 1)
                    gracz2[0].kosc5 = random.randrange(1, 6, 1)
                    gracz2[0].ruch += 1
                    gracz2[0].wynik = gracz2[0].wynik
                    gracz2[0].save()
        else:
            if gracz1:
                if gracz1[0].ruch >= gracz2[0].ruch:
                    #  kiedy juz wykonał ruch i gracz2 też
                    gracz2[0].imie = "gracz2"
                    if not 'kosc1' in some_var:
                        gracz2[0].kosc1 = random.randrange(1, 6, 1)
                    if not 'kosc2' in some_var:
                        gracz2[0].kosc2 = random.randrange(1, 6, 1)
                    if not 'kosc3' in some_var:
                        gracz2[0].kosc3 = random.randrange(1, 6, 1)
                    if not 'kosc4' in some_var:
                        gracz2[0].kosc4 = random.randrange(1, 6, 1)
                    if not 'kosc5' in some_var:
                        gracz2[0].kosc5 = random.randrange(1, 6, 1)
                    gracz2[0].ruch += 1
                    if gracz2[0].ruch % 2 == 0:  # już po inkrementacji czyli mozna zliczyć wynik rundy
                        gracz2[0].wynik += obliczWynik(gracz2[0].kosc1, gracz2[0].kosc2, gracz2[0].kosc3,
                                                       gracz2[0].kosc4, gracz2[0].kosc5)

                    gracz2[0].save()

        h = GraHistoria(nrHist=GraHistoria.objects.all().count() + 1, imie=gracz2[0].imie, kosc1=gracz2[0].kosc1,
                        kosc2=gracz2[0].kosc2, kosc3=gracz2[0].kosc3, kosc4=gracz2[0].kosc4, kosc5=gracz2[0].kosc5,
                        ruch=gracz2[0].ruch, nrGry=gracz2[0].nrGry, wynik=gracz2[0].wynik)

        print("\n\n HIST G2 ADD", h.nrHist, h.imie, h.ruch, h.wynik, h.nrGry, "\n\n\n")
        h.save()

        if gracz1:
            return render(request, 'kosci/gracz2.html',
                          {'kosc1': gracz2[0].kosc1, 'kosc2': gracz2[0].kosc2, 'kosc3': gracz2[0].kosc3,
                           'kosc4': gracz2[0].kosc4, 'kosc5': gracz2[0].kosc5, 'ruchg1': gracz1[0].ruch,
                           'ruchg2': gracz2[0].ruch, 'wynikg1': gracz1[0].wynik, 'wynikg2': gracz2[0].wynik})
        else:
            return render(request, 'kosci/gracz2.html',
                          {'kosc1': gracz2[0].kosc1, 'kosc2': gracz2[0].kosc2, 'kosc3': gracz2[0].kosc3,
                           'kosc4': gracz2[0].kosc4, 'kosc5': gracz2[0].kosc5, 'ruchg1': "",
                           'ruchg2': gracz2[0].ruch, 'wynikg1': "", 'wynikg2': gracz2[0].wynik})
