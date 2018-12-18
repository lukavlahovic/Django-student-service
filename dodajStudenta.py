import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()
from studserviceapp.models import Student, Grupa, Semestar, Nalog,IzborGrupe

IzborGrupe.objects.all().delete()
Student.objects.all().delete()
Nalog.objects.get(username='lvlahovic16', lozinka='44387294', uloga='student').delete()
Nalog.objects.get(username='mmitrovic16', lozinka='204921', uloga='student').delete()
Nalog.objects.get(username='l_jelic17', lozinka='57788249', uloga='student').delete()
Nalog.objects.get(username='a_petrovic17', lozinka='16464863', uloga='student').delete()

grupa1 = Grupa.objects.get(oznaka_grupe='303')
grupa2 = Grupa.objects.get(oznaka_grupe='302')
grupa3 = Grupa.objects.get(oznaka_grupe='314')
grupa4 = Grupa.objects.get(oznaka_grupe='303')


n3 = Nalog(username='lvlahovic16', lozinka='44387294', uloga='student')
n3.save()
n4 = Nalog(username='mmitrovic16', lozinka='204921', uloga='student')
n4.save()
n1 = Nalog(username='l_jelic17', lozinka='57788249', uloga='student')
n1.save()
n2 = Nalog(username='a_petrovic17', lozinka='16464863', uloga='student')
n2.save()

s3 = Student(ime='Luka',prezime='Vlahovic',godina_upisa=2016,broj_indeksa=22,smer='RN',nalog=n3)
s3.save()
s4 = Student(ime='Marko',prezime='Mitroivc',godina_upisa=2016,broj_indeksa=65,smer='RM',nalog=n4)
s4.save()
s1 = Student(ime='Luka',prezime='Jelic',godina_upisa=2017, broj_indeksa=90,smer='RN',nalog=n1)
s1.save()
s2 = Student(ime='Andrija',prezime='Petrovic',godina_upisa=2017, broj_indeksa=85,smer='RN',nalog=n2)
s2.save()

s1.grupa.add(grupa1)
s2.grupa.add(grupa2)
s3.grupa.add(grupa3)
s4.grupa.add(grupa4)
