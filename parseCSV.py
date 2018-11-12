import csv
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar

def razdvojImeiPrezime(s):

    l = -len(s)
    for i in range(-1, l, -1):
        p = s[0:i]
        if p[len(p) - 1] == ' ':      #vraca prvi element niza ime, a drugi prezime
            p = p[0:-1]
            break;
    return s[len(p) + 1:], p


def napraviUsername(ime, prezime):

    i = ime[0].lower()
    p = prezime.replace(' ','').lower()   #vraca strig za username profesora
    return i+p

def razdvojGrupe(grupe):

    return grupe.split(', ')

def razdvojVreme(vreme):

    return vreme.split('-')




def import_timetable_from_csv(file_path):
    with open(file_path,encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        next(raspored_csv, None)
        next(raspored_csv, None)
        a = 1
        b = 0
        skupNastavnika = set()
        skupGrupa = set()
        semester = Semestar(vrsta='neparni', skolska_godina_pocetak=2018, skolska_godina_kraj=2019)
        semester.save()
        rasporedNastave = RasporedNastave(datum_unosa=datetime.datetime.today(),semestar=semester)
        rasporedNastave.save()
        for _red in raspored_csv:
            if b == 1:
                b = 0
                continue
            if not _red:
                a = 1
                continue
            if a == 1:
                stringPredmet = _red[0]
                predmet = Predmet.objects.create(naziv=stringPredmet)
                predmet.save()
                a = 0
                b = 1
            else:
                i = 1
                while i < 32:
                    if _red[i] == '':
                        i = i + 8
                        continue
                    else:
                        if i == 1:
                            tip = 'predavanja'
                        else:
                            if i == 9:
                                tip = 'praktikum'
                            else:
                                if i == 17:
                                    tip = 'vezbe'
                                else:
                                    tip = 'predavanjavezbe'
                        stringNastavnik = _red[i]
                        imePrezime = razdvojImeiPrezime(stringNastavnik)
                        if stringNastavnik not in skupNastavnika:
                            skupNastavnika.add(stringNastavnik)
                            #jos razdvajanje stringa i pravljenje objekta nastavnik i njegov nalog
                            username = napraviUsername(imePrezime[0],imePrezime[1])
                            nalog = Nalog(username=username, uloga='nastavnik')
                            nalog.save()
                            nastavnik = Nastavnik(ime=imePrezime[0],prezime=imePrezime[1],nalog=nalog)
                            nastavnik.save()
                        nastavnik = Nastavnik.objects.get(ime=imePrezime[0],prezime=imePrezime[1])
                        if predmet not in nastavnik.predmet.all():
                            nastavnik.predmet.add(predmet)
                            nastavnik.save()

                        i = i + 2
                        stringOdeljenja = _red[i]
                        odeljenja = razdvojGrupe(stringOdeljenja)

                        #razdvojiti odeljenja iz stringa
                        i = i + 2
                        dan = _red[i]
                        i = i + 1
                        stringVreme = _red[i]
                        vreme = razdvojVreme(stringVreme)
                        pocetak = vreme[0]
                        kraj = vreme[1]+':00'
                        #razdvojiti na pocetak i kraj
                        i = i + 1
                        ucionica = _red[i]
                        termin = Termin(oznaka_ucionice=ucionica, pocetak=pocetak, zavrsetak=kraj, dan=dan,tip_nastave=tip,nastavnik=nastavnik,predmet=predmet, raspored=rasporedNastave)
                        termin.save()
                        for g in odeljenja:
                            if g not in skupGrupa:
                                skupGrupa.add(g)
                                o = Grupa.objects.create(oznaka_grupe=g,semestar=semester)
                            o = Grupa.objects.get(oznaka_grupe=g,semestar=semester)
                            termin.grupe.add(o)
                            termin.save()
                        i = i + 2






RasporedNastave.objects.all().delete()
Grupa.objects.all().delete()
Nastavnik.objects.all().delete()
Semestar.objects.all().delete()
Termin.objects.all().delete()
Predmet.objects.all().delete()
Nalog.objects.all().delete()

import_timetable_from_csv('rasporedCSV.csv')
