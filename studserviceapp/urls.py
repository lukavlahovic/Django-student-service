from django.urls import path
from . import views

urlpatterns = [
         path("",views.index,name='index') ,
         path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
]