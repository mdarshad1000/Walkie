from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.
rooms = [
    {'id':1, 'name':'Lets learn Flask!'},
    {'id':2, 'name':'100 Days of Code'},
    {'id':3, 'name':'CI CD in one shot'},
]


def home(request):
    # Querying the Room
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)  # {'how to address in template':what to pass}
    

def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room':room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)