
from django.http import HttpResponse

def index(request):
    return HttpResponse("Dobrodosli na studentski servis")

