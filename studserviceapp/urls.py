from django.urls import path
from . import views

urlpatterns = [
         path("",views.index,name='index') ,
         path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
         path("nastavnici",views.nastavnici_template,name='nastavnici_template') ,
         path('unosobv/<str:user>', views.unos_obavestenja_form, name='unosobavestenja'),
         path("saveobavestenje",views.save_obavestenje,name='saveobavestenje') ,
         path('izbornagrupa',views.izborna_grupa_form,name='izbornagrupa') ,
         path("saveizbornagrupa", views.saveizbornagrupa,name='saveizbornagrupa'),
         path('izmenagrupe/<str:oznakaGrupe>', views.izmenaIzborneGrupe, name='izmenagrupe'),
         path("saveizmenagrupa", views.sacuvanaIzmenaGrupe,name='saveizmenagrupa'),
]