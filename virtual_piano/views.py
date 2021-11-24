from django.shortcuts import render

# Create your views here.


def piano(request):
    if request.method == 'POST':
        pressed = request.POST.get('pressed')
        print(pressed)
    return render(request, 'virtual_piano/piano.html', {})
