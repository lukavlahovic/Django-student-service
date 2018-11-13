
from django.http import HttpResponse
from django.shortcuts import render
import datetime

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, Student, \
    Obavestenje, IzbornaGrupa


def index(request):
    return HttpResponse('Pozdrav')

def timetableforuser(request, username):


  if username[len(username)-1].isdigit()!=True:
    n = Nalog.objects.get(username=username)
    s = Termin.objects.all().filter(nastavnik=Nastavnik.objects.get(nalog=n))
    r = ''
    c =''
    for a in s:
        c =''
        g = a.grupe.all()
        for l in g:
            c = c + l.oznaka_grupe+ ' '
        r = r +'<pre>'+ a.oznaka_ucionice+' |'+a.pocetak.strftime('%H:%M')+'-'+a.zavrsetak.strftime('%H:%M') + ' |'+ a.dan+' |'+ a.tip_nastave + ' |'+ a.predmet.naziv+' |'+c + ' |'+'</pre>'



    return HttpResponse(r)
  else:
      n = Nalog.objects.get(username=username)
      s = Student.objects.get(nalog=n)
      g = Grupa.objects.get(student=s)

      t = Termin.objects.all().filter(grupe=g)
      r = ''
      for a in t:
          j = a.grupe.all()
          c = ''
          for l in j:
              c = c + l.oznaka_grupe + ' '
          r = r +'<pre>'+ a.oznaka_ucionice + ' |' + a.pocetak.strftime('%H:%M') + '-' + a.zavrsetak.strftime('%H:%M') + ' |' + a.dan + ' |' + a.tip_nastave + ' |' + a.predmet.naziv +' |'+a.nastavnik.ime+' '+a.nastavnik.prezime+ ' |' + c + ' |'+'</pre>'


      return HttpResponse(r)



def nastavnici_template(request):
    qs = Nastavnik.objects.all()
    context = { 'nastavnici' : qs}
    return render(request,'studserviceapp/nastavnici.html', context)


def unos_obavestenja_form(request,user):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga=='sekretar' or n.uloga=='administrator':
            context = {'nalog':n}
            return render(request, 'studserviceapp/unosobavestenja.html',
                          context)
        else: return HttpResponse('<h1>Korisnik mora biti sekretar ili administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')


def save_obavestenje(request):
    tekst = request.POST['tekst']
    postavio = Nalog.objects.get(username=request.POST['postavio'])
    obavestenje = Obavestenje(tekst=tekst,postavio=postavio,datum_postavljanja=datetime.datetime.now())
    obavestenje.save()
    return HttpResponse('<h1>Obavestenje sačuvano</h1>')

def izborna_grupa_form(request):

    qs = Predmet.objects.all()
    context = { 'predmeti' : qs}
    return render(request, 'studserviceapp/izbornaGrupa.html', context)

def saveizbornagrupa(request):

    vrsta = request.POST['vrsta']
    skolska_godina_pocetak = request.POST['skolska_godina_pocetak']
    skolska_godina_kraj = request.POST['skolska_godina_kraj']
    oznaka_semestra = request.POST['oznaka_semestra']
    oznaka_grupe = request.POST['oznaka_grupe']
    kapacitet = request.POST['kapacitet']
    smer = request.POST['smer']
    aktivna = request.POST.get('aktivna',False)

    predmeti = request.POST.getlist("predmeti")

    try:
        semestar = Semestar.objects.get(vrsta=vrsta, skolska_godina_kraj=skolska_godina_kraj,skolska_godina_pocetak=skolska_godina_pocetak)
    except Semestar.DoesNotExist:
        semestar = Semestar(vrsta=vrsta, skolska_godina_kraj=skolska_godina_kraj,skolska_godina_pocetak=skolska_godina_pocetak)
        semestar.save()

    izbornaGrupa = IzbornaGrupa(oznaka_grupe=oznaka_grupe,kapacitet=kapacitet,oznaka_semestra=oznaka_semestra,smer=smer,aktivna=aktivna,za_semestar=semestar)
    izbornaGrupa.save()
    for predmet in predmeti:
        p = Predmet.objects.get(id=predmet)
        izbornaGrupa.predmeti.add(p)
    izbornaGrupa.save()


    return izborna_grupa_form(request)


def izmenaIzborneGrupe(request, oznakaGrupe):

    try:
        g = IzbornaGrupa.objects.get(oznaka_grupe=oznakaGrupe)
        p = Predmet.objects.all()
        context = {'grupa':g, 'predmeti':p}
        return render(request, 'studserviceapp/izmenaIzbornaGrupa.html',
                          context)

    except IzbornaGrupa.DoesNotExist:
        return HttpResponse('Grupa ne postoji')

def sacuvanaIzmenaGrupe(request):

    #izmenjeni podaci stare grupe
    staraGrupa = request.POST['grupaID']
    vrsta = request.POST['vrsta']
    skolska_godina_pocetak = request.POST['skolska_godina_pocetak']
    skolska_godina_kraj = request.POST['skolska_godina_kraj']
    oznaka_semestra = request.POST['oznaka_semestra']
    oznaka_grupe = request.POST['oznaka_grupe']
    kapacitet = request.POST['kapacitet']
    smer = request.POST['smer']
    aktivna = request.POST.get('aktivna', False)

    predmeti = request.POST.getlist("predmeti")

    try:
        semestar = Semestar.objects.get(vrsta=vrsta, skolska_godina_kraj=skolska_godina_kraj,
                                        skolska_godina_pocetak=skolska_godina_pocetak)
    except Semestar.DoesNotExist:
        semestar = Semestar(vrsta=vrsta, skolska_godina_kraj=skolska_godina_kraj,skolska_godina_pocetak=skolska_godina_pocetak)
        semestar.save()

    izbornaGrupa = IzbornaGrupa.objects.get(id=staraGrupa)
    izbornaGrupa.oznaka_grupe=oznaka_grupe
    izbornaGrupa.oznaka_semestra = oznaka_semestra
    izbornaGrupa.kapacitet = kapacitet
    izbornaGrupa.smer = smer
    izbornaGrupa.aktivna = aktivna

    for predmet in izbornaGrupa.predmeti:
        izbornaGrupa.predmeti.remove(predmet)

    for predmet in predmeti:
        p = Predmet.objects.get(id=predmet)
        izbornaGrupa.predmeti.add(p)

    izbornaGrupa.save()


    return HttpResponse("Izmene sacuvane")