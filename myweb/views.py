from django.shortcuts import render
from django.conf import settings

# Passing FontAwesome 5 Key 
#https://stackoverflow.com/questions/433162/can-i-access-constants-in-settings-py-from-templates-in-django
def home(request):
    context = {'FONTAWESOME_KEY': settings.FONTAWESOME_KEY}
    return render(request, 'home.html', context)
