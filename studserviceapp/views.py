
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import parseCSV
import send_gmails

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, Student, \
    Obavestenje, IzbornaGrupa, IzborGrupe, TerminPolaganja, RasporedPolaganja, Attachment


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
        p.semestar_po_programu = oznaka_semestra
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
    izbornaGrupa.za_semestar=semestar
    izbornaGrupa.oznaka_grupe=oznaka_grupe
    izbornaGrupa.oznaka_semestra = oznaka_semestra
    izbornaGrupa.kapacitet = kapacitet
    izbornaGrupa.smer = smer
    izbornaGrupa.aktivna = aktivna

    for predmet in izbornaGrupa.predmeti.all():
        izbornaGrupa.predmeti.remove(predmet)

    for predmet in predmeti:
        p = Predmet.objects.get(id=predmet)
        p.semestar_po_programu = oznaka_semestra
        izbornaGrupa.predmeti.add(p)

    izbornaGrupa.save()


    return HttpResponse("Izmene sacuvane")





def izborGrupe(request, studentUserName):

    try:
        n = Nalog.objects.get(username=studentUserName)
        s: Student = Student.objects.get(nalog=n)
        semestar = Semestar.objects.last()
        for ig in IzborGrupe.objects.filter(student=s):
            if ig.izabrana_grupa.za_semestar == semestar:
                return HttpResponse('Ovaj nalog je vec izabrao grupu')

        izbornagrupa = IzbornaGrupa.objects.filter(smer=s.smer,aktivna=True,za_semestar=semestar)
        p = Predmet.objects.all()

        lista = []
        for g in izbornagrupa:
            if IzborGrupe.objects.filter(izabrana_grupa=g).count() < g.kapacitet:
                lista.append(g)

        context = {'nalog':n,'student': s, 'semestar': semestar, 'izbornagrupa': izbornagrupa, 'lista': lista, 'predmeti':p}
        return render(request, 'studserviceapp/izborGrupe.html',
                          context)

    except Nalog.DoesNotExist:
        return HttpResponse('Nalog ne postoji')


def sacuvajIzborGrupe(request):


    ostvarenoESPB = request.POST['ostvarenoESPB']
    upisujeESPB = request.POST['upisujeESPB']
    broj_polozenih_ispita = request.POST['broj_polozenih_ispita']
    upisuje_semestar = request.POST.get('upisuje_semestar',False)
    prvi_put_upisuje_semestar = request.POST.get('prvi_put_upisuje_semestar',False)
    izabrana_grupa = request.POST['izabrana_grupa']
    grupa = IzbornaGrupa.objects.get(id=izabrana_grupa)
    nepolozeni_predmeti = request.POST.getlist("nepolozeni_predmeti")
    nacin_placanja = request.POST['nacin_placanja']
    studentID = request.POST['studentID']

    student = Student.objects.get(id=studentID)

    izborgrupe = IzborGrupe(ostvarenoESPB=ostvarenoESPB,upisujeESPB=upisujeESPB,broj_polozenih_ispita=broj_polozenih_ispita,
                            upisuje_semestar=upisuje_semestar,prvi_put_upisuje_semestar=prvi_put_upisuje_semestar,
                            nacin_placanja=nacin_placanja,student=student,
                            izabrana_grupa=grupa,upisan=False)
    izborgrupe.save()

    for predmet in nepolozeni_predmeti:
        p = Predmet.objects.get(id=predmet)
        izborgrupe.nepolozeni_predmeti.add(p)

    return HttpResponse("sacuvano")

def ispisGrupa(request):

    izbornagrupa = IzbornaGrupa.objects.all()
    context = {'izbornagrupa':izbornagrupa}
    return render(request, 'studserviceapp/ispisGrupa.html',
                  context)

def ispisGrupaID(request,grupaID):

    izbornagrupa = IzbornaGrupa.objects.get(id=grupaID)
    izborgrupe = IzborGrupe.objects.filter(izabrana_grupa=izbornagrupa)

    lista = []
    for ig in izborgrupe:
        lista.append(ig.student)

    context = {'lista': lista}
    return render(request, 'studserviceapp/ispisStudenta.html',
                  context)


def uploadSlike(request, studentUserName):
    nalog = Nalog.objects.get(username=studentUserName)
    student = Student.objects.get(nalog=nalog)

    context = {'student': student,'nalog':nalog}
    return render(request, 'studserviceapp/uploadSlike.html',context)

def savesliku(request):
    slika = request.FILES['image']
    username = request.POST['nalog']
    print(username)
    nalog = Nalog.objects.get(username=username)
    student = Student.objects.get(nalog=nalog)
    student.slika = slika
    student.save()
    return HttpResponse("radi")

def predmeti_profesor(request, username):
    nalog = Nalog.objects.get(username=username)
    nastavnik = Nastavnik.objects.get(nalog=nalog)

    termini = Termin.objects.all().filter(nastavnik=nastavnik)
    recnik = {}

    for t in termini:
        p = t.predmet
        lista = []
        if recnik.get(p.naziv) is None:
            for g in t.grupe.all():
                lista.append(g)
        else:
            lista = recnik.get(p.naziv)
            for g in t.grupe.all():
                lista.append(g)

        recnik.setdefault(p.naziv, lista)

    context = {'nalog':nalog,'nastavnik': nastavnik, 'recnik': recnik}
    return render(request, 'studserviceapp/predmetiProfesor.html', context)

def grupe_sa_slikama(request,username,grupaID):
    nalog = Nalog.objects.get(username=username)
    grupa = Grupa.objects.get(id=grupaID)
    studenti = Student.objects.all().filter(grupa=grupa)

    context = {'nalog':nalog,'studenti': studenti}
    return render(request, 'studserviceapp/ispisStudentaSaSlikom.html',
                  context)

def prikaz_slike(request,username,studentID):
    nalog = Nalog.objects.get(username=username)
    student = Student.objects.get(id=studentID)
    context = {'nalog':nalog,'student': student}
    return render(request, 'studserviceapp/prikazslike.html',
                  context)

def upload_kolokvijum(request):
    return render(request,'studserviceapp/uploadKolokvijum.html')

def savekolokvijum(request):
    kolokvijumska_nedelja = request.POST['kolokvijum']
    file_path = request.FILES['fajl_kolokvijum']
    file_data = file_path.read().decode("utf-8")
    greske = parseCSV.import_kolokvijum_from_csv(file_data,kolokvijumska_nedelja)
    recnik = {}
    for k,v in greske[0].items():
        s=""
        for e in v:
            s+=(str(e) + ";")
        recnik.setdefault(k,s)
       # print(recnik.get(k))
    context = {'greska':recnik,'podaci':greske[1],'kolokvijumska_nedelja':kolokvijumska_nedelja}
    return render(request,'studserviceapp/prikazGresaka.html',context)

def izmenicu_sam(request):
    kolokvijumska_nedelja = request.POST['kolokvijumska_nedelja']
    print(kolokvijumska_nedelja)
    rp = RasporedPolaganja.objects.get(kolokvijumska_nedelja=kolokvijumska_nedelja)
    for t in TerminPolaganja.objects.all().filter(raspored_polaganja=rp):
        t.delete()
    rp.delete()
    return render(request,'studserviceapp/uploadKolokvijum.html')

def forma_ispravak(request,broj_reda):
    podaci = request.POST.getlist("podaci")
    print("podaci =",end=" ")
    print(podaci)
    return render(request,'studserviceapp/formaIspravak.html')

def slanje_mejla(request,username):
    #provera da li nalog postoji
    try:
        nalog = Nalog.objects.get(username=username)
    except:
        return HttpResponse("Nalog ne postoji")
    #provera uloge
    if nalog.uloga == 'student':
        return HttpResponse("Studnet nema pravo pristupa")

    elif nalog.uloga == 'nastavnik':
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        termini = Termin.objects.all().filter(nastavnik=nastavnik)
        recnik = {}
        p_lista = []
        g_lista = []
        for t in termini:
            p = t.predmet
            if not p in p_lista:
                p_lista.append(p)
            for g in t.grupe.all():
                if not g in g_lista:
                    g_lista.append(g)
            """
            if recnik.get(p.naziv) is None:
                for g in t.grupe.all():
                    lista.append(g)
            else:
                lista = recnik.get(p.naziv)
                for g in t.grupe.all():
                    lista.append(g)

            recnik.setdefault(p.naziv, lista)
"""
        context = {'nalog':nalog,'nastavnik': nastavnik, 'predmeti': p_lista,'grupe':g_lista}

        return render(request,'studserviceapp/slanjeMejla.html',context)

    elif nalog.uloga == 'sekretar' or nalog.uloga == 'administrator':
        predmeti = Predmet.objects.all()
        termini = Termin.objects.all()
        lista1 = []
        smerovi = []
        for t in termini:
            for g in t.grupe.all():
                if g in lista1:
                    continue
                lista1.append(g)
                if g.smer in smerovi:
                    continue
                smerovi.append(g.smer)
    context = {'nalog':nalog,'predmeti':predmeti,'grupe':lista1,'smerovi':smerovi}
    return render(request, 'studserviceapp/slanjeMejla.html',context)

def posalji_mejl(request):
    nalog_str = request.POST['nalog']
    nalog = Nalog.objects.get(username=nalog_str)
    naslov = request.POST['naslov']
    tekst = request.POST['tekst']
    try:
        attach = request.FILES['attach']
        attachment = Attachment.objects.create(fajl=attach)
        attachment_str = str(attachment.fajl)
        dir = 'D:/' + attachment_str
    except:
        attach = None
        dir = None
    username = nalog.username + "@raf.rs"
    izbor = request.POST.getlist('izbor')
    print(izbor)
    for i in izbor:
        if i =="svi":
            svi_studenti = Student.objects.all()
            for s in svi_studenti:
                primalac = s.nalog.username + '@raf.rs'
                send_gmails.create_and_send_message("lvlahovic16@raf.rs", primalac, naslov, tekst, dir, None)
        if i == 'RN' or i=='RM':
            studlista = []
            tmp = Grupa.objects.all().filter(smer=i)
            for g in tmp:
                studneti = Student.objects.all().filter(grupa=g)
                for s in studneti:
                    studlista.append(s)
            for s in studlista:
                primalac = s.nalog.username + '@raf.rs'
                send_gmails.create_and_send_message("lvlahovic16@raf.rs", primalac, naslov, tekst, dir, None)

        try:
            tmp = Predmet.objects.get(naziv=i)
            print("radi predmet")
            print(tmp)
            s_lista = []
            termini = Termin.objects.all().filter(predmet=tmp,tip_nastave='predavanja')
            for t in termini:
                for g in t.grupe.all():
                    studneti = Student.objects.all().filter(grupa=g)
                    for s in studneti:
                        s_lista.append(s)
            for s in s_lista:
                primalac = s.nalog.username + '@raf.rs'
                send_gmails.create_and_send_message("lvlahovic16@raf.rs", primalac, naslov, tekst, dir, None)
        except:
            print("predmet except")
        try:
            tmp = Grupa.objects.get(oznaka_grupe=i)
            print("radi grupu")
            studneti1 = Student.objects.all().filter(grupa=tmp)
            for s in studneti1:
                primalac = s.nalog.username + '@raf.rs'
                send_gmails.create_and_send_message("lvlahovic16@raf.rs", primalac, naslov, tekst, dir, None)
        except:
            print("grupa except")


    #send_gmails.create_and_send_message("lvlahovic16@raf.rs","a_petrovic17@raf.rs",naslov,tekst,dir,None)


    return HttpResponse("mejl poslat")

def logovanje(request):
    return render(request,'studserviceapp/logovanje.html')

def pomocna(request):
    username = request.POST['nalog']
    try:
        nalog = Nalog.objects.get(username=username)
    except:
        return HttpResponse("Nalog ne postoji")
    url = 'pocetni_ekran/' + username
    return redirect(url)

def pocetni_ekran(request,username):
    #username = request.POST['nalog']
    try:
        nalog = Nalog.objects.get(username=username)
    except:
        return HttpResponse("Nalog ne postoji")

    if nalog.uloga == "student":
        s = Student.objects.get(nalog=nalog)
        g = Grupa.objects.get(student=s)

        t = Termin.objects.all().filter(grupe=g)
        context = {'nalog':nalog,'termini':t}
        return render(request, 'studserviceapp/pocetniEkranStudent.html', context)

    elif nalog.uloga == "nastavnik":
        s = Termin.objects.all().filter(nastavnik=Nastavnik.objects.get(nalog=nalog))
        context = {'nalog':nalog,'termini':s}
        return render(request, 'studserviceapp/pocetniEkranNastavnik.html', context)

    elif nalog.uloga == "sekretar":
        termini = Termin.objects.all()
        context = {'nalog': nalog,'termini':termini}
        return render(request, 'studserviceapp/pocetniEkranSekretar.html', context)

    else:
        termini = Termin.objects.all()
        context = {'nalog':nalog,'termini':termini}
        return render(request, 'studserviceapp/BasedStudent.html', context)

def raspored_nastave(request,username):
    t = Termin.objects.all()
    nalog = Nalog.objects.get(username=username)
    context = {'nalog': nalog, 'termini': t}
    return render(request, 'studserviceapp/raspored_nastave.html', context)