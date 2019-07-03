from django.http import HttpResponse

def home(request):
    return HttpResponse("Test view Django.")