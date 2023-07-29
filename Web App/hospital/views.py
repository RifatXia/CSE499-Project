from django.shortcuts import render, redirect
from .forms import PersonForm

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PersonForm()

    return render(request, 'hospital/add_person.html', {'form': form})


def success(request):
    return render(request, 'hospital/success.html')