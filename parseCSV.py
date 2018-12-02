import csv
import time
from datetime import datetime
import datetime
from dateutil import parser
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from csv import reader
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, IzborGrupe, IzbornaGrupa

def razdvojImeiPrezime(s):

    s = s.strip()
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


def import_kolokvijum_from_csv(file_path):
   lines = file_path.split('\n')
   lines = lines[1::]
   brojac = 2
   greske = {}


   for red in reader(lines):
       #izvlacimo predmet - red[0]
       predmet = None
       nastavnik = None
       try:
           predmet = Predmet.objects.get(naziv=red[0])
       except Predmet.DoesNotExist:
           lista = []
           if greske.get(brojac) is None:
                   lista.append('Ne postoji predmet u bazi')
           else:
               lista = greske.get(brojac)
               lista.append('Ne postoji predmet u bazi')
           greske.setdefault(brojac, lista)


       #izvlacimo ime profesora - red[3]
       profesori = red[3].split(",")
       for p in profesori:
           imeiprezime = razdvojImeiPrezime(p)
           ime = imeiprezime[0]
           prezime = imeiprezime[1]
           try:
               nastavnik = Nastavnik.objects.get(ime=ime,prezime=prezime)
           except Nastavnik.DoesNotExist:
               try:
                   nastavnik = Nastavnik.objects.get(ime=prezime, prezime=ime)
               except Nastavnik.DoesNotExist:
                   lista = []
                   if greske.get(brojac) is None:
                       lista.append('Ne postoji nastavnik u bazi')
                   else:
                       lista = greske.get(brojac)
                       lista.append('Ne postoji nastavnik u bazi')
                   greske.setdefault(brojac, lista)

       #izvlacimo ucionica - red[4]
       ucionice = red[4]
       #izvlacimo vreme - red[5]
       vreme = razdvojVreme(red[5])
       pocetak = vreme[0]+ ':00'
       kraj = vreme[1] + ':00'
       #izvlacimo dan - red[6]/////NIJE U MODELU

       #izvlacimo datum - red[7]
       datumcsv = red[7].split('.')
       datum = datumcsv[0]+'/'+datumcsv[1]+'/'+str(datetime.datetime.today().year)
       datum = datetime.datetime.strptime(datum,'%d/%m/%Y').date()


       brojac+=1
      # spisak = greske.get(brojac-1)
      # try:
           #for s in spisak:
             # print(s,end=' ')
      # except:
           #print(spisak,end='')
      # print()
       try:
           print(predmet.naziv, nastavnik.ime,ucionice, pocetak, kraj, datum)
       except:
           print("Nema")




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
        rasporedNastave = RasporedNastave(datum_unosa=datetime.datetime.today(), semestar=semester)
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




#IzborGrupe.objects.all().delete()
#IzbornaGrupa.objects.all().delete()
#Semestar.objects.all().delete()
#RasporedNastave.objects.all().delete()
#Grupa.objects.all().delete()
#Nastavnik.objects.all().delete()
#Termin.objects.all().delete()
#Predmet.objects.all().delete()
#Nalog.objects.all().delete()

#import_timetable_from_csv('rasporedCSV.csv')
