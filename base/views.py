from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.
# rooms = [
#     {'id':1, 'name':'Lets learn Flask!'},
#     {'id':2, 'name':'100 Days of Code'},
#     {'id':3, 'name':'CI CD in one shot'},
# ]


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

    context = {}
    return render(request, 'base/login_register.html', context)


def home(request):
    # Querying the Room if query matches or contains the query entered.
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    '''
    Q --> so that we can serach not just by topic, but by name, description etc
    | --> stands for OR
    '''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
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


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # `instance` is so that the form we get is pre filled
    form = RoomForm(instance=room)

    if request.method == 'POST':
        # `instance` here will replace the pre filled value
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})