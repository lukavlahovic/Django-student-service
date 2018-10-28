import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from studserviceapp.models import Student, Grupa, Semestar, Nalog

Student.objects.all().delete()
Grupa.objects.all().delete()
Semestar.objects.all().delete()
Nalog.objects.all().delete()

semestar = Semestar(vrsta = 'neparni', skolska_godina_pocetak=2018, skolska_godina_kraj=2019)
semestar.save()

n1 = Nalog(username='l_jelic17', lozinka='57788249', uloga='student')
n1.save()

g303 = Grupa.objects.create(oznaka_grupe='303', smer='RN', semestar=semestar)
g304 = Grupa.objects.create(oznaka_grupe='304', smer='RN', semestar=semestar)


s1 = Student(ime='Luka',prezime='Jelic',godina_upisa=2017, broj_indeksa=90,smer='RN',nalog=n1)
s1.save()
s1.grupa.add(g303)


n2 = Nalog(username='a_petrovic17', lozinka='16464863', uloga='student')
n2.save()
s2 = Student(ime='Andrija',prezime='Petrovic',godina_upisa=2017, broj_indeksa=85,smer='RN',nalog=n2)
s2.save()
s2.grupa.add(g303)
s2.grupa.add(g304)
print(s1 in Student.objects.all())
Student.objects.all().delete()
Grupa.objects.all().delete()
Semestar.objects.all().delete()
Nalog.objects.all().delete()




