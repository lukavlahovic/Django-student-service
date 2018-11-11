
from django.http import HttpResponse
from django.shortcuts import render
import datetime

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, Student, \
    Obavestenje


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