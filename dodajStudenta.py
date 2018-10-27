import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from studserviceapp.models import Student, Grupa, Semestar, Nalog

semestar = Semestar(vrsta = 'neparni', skolska_godina_pocetak=2018, skolska_godina_kraj=2019)
semestar.save()
g303: Grupa = Grupa(oznaka_grupe='303', smer='RN', semestar=semestar)

n1 = Nalog(username='l_jelic17', lozinka='57788249', uloga='student')
n1.save()


s1 = Student(ime='Luka',prezime='Jelic',godina_upisa=2017, broj_indeksa=90,smer='RN',nalog=n1)
s1.save()
s1.grupa.add(g303)


n2 = Nalog(username='a_petrovic17', lozinka='16464863', uloga='student')
n2.save()
s2 = Student(ime='Andrija',prezime='Petrovic',godina_upisa=2017, broj_indeksa=85,smer='RN',nalog=n2,grupa = g303)
s2.save()



