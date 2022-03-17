from django.shortcuts import render
from .models import Mindspace

# Create your views here.
def simpleView(request):
    objects = Mindspace.objects.all()
    context = {'objects': objects}
    return render(request, 'index.html', context)