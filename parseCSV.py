import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentskiServis.settings")
import django
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet

def import_timetable_from_csv(file_path):
    with open(file_path,encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        next(raspored_csv,None)
        next(raspored_csv, None)
        a = 1
        b = 0
        for _red in raspored_csv:
            if b == 1:
                b = 0
                continue
            if not _red:
                a = 1
                continue
            if a == 1:
                print(_red[0])
                a = 0
                b = 1
            else:
                print(len(_red))





import_timetable_from_csv('rasporedCSV.csv')
