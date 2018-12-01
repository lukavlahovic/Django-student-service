from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path("nastavnici", views.nastavnici_template, name='nastavnici_template'),
    path('unosobv/<str:user>', views.unos_obavestenja_form, name='unosobavestenja'),
    path("saveobavestenje", views.save_obavestenje, name='saveobavestenje'),
    path('izbornagrupa', views.izborna_grupa_form, name='izbornagrupa'),
    path("saveizbornagrupa", views.saveizbornagrupa, name='saveizbornagrupa'),
    path('izmenagrupe/<str:oznakaGrupe>', views.izmenaIzborneGrupe, name='izmenagrupe'),
    path("saveizmenagrupa", views.sacuvanaIzmenaGrupe, name='saveizmenagrupa'),
    path('izborgrupe/<str:studentUserName>', views.izborGrupe, name='izborgrupe'),
    path("sacuvajizborgrupe", views.sacuvajIzborGrupe, name='sacuvajizborgrupe'),
    path("ispisgrupa", views.ispisGrupa, name='ispisgrupa'),
    path('ispisgrupa/<str:grupaID>', views.ispisGrupaID, name='ispisgrupaID'),
    path('uploadslike/<str:studentUserName>', views.uploadSlike, name='uploadslike'),
    path('savesliku', views.savesliku, name='savesliku'),
    path('prikazpredmeta/<str:username>', views.predmeti_profesor, name='prikazpredmeta'),
    path('prikazgrupe/<str:grupaID>', views.grupe_sa_slikama, name='prikazgrupe'),
    path('prikazslike/<str:studentID>', views.prikaz_slike, name='prikazslike'),
]