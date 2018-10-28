
from django.http import HttpResponse
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar,Student

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
        r = r + a.oznaka_ucionice+' |'+a.pocetak.strftime('%H:%M')+'-'+a.zavrsetak.strftime('%H:%M') + ' |'+ a.dan+' |'+ a.tip_nastave + ' |'+ a.predmet.naziv+' |'+c + ' |'

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
          r = r + a.oznaka_ucionice + ' |' + a.pocetak.strftime('%H:%M') + '-' + a.zavrsetak.strftime('%H:%M') + ' |' + a.dan + ' |' + a.tip_nastave + ' |' + a.predmet.naziv +' |'+a.nastavnik.ime+' '+a.nastavnik.prezime+ ' |' + c + ' |'

      return HttpResponse(r)



