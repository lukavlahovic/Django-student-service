import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet

def import_timetable_from_csv(file_path):
    with open(file_path,encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        for _red in raspored_csv:


