import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()
from studserviceapp.models import  Nalog

n1 = Nalog(username='marbutina', lozinka='', uloga='sekretar')
n1.save()