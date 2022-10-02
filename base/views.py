from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.
# rooms = [
#     {'id':1, 'name':'Lets learn Flask!'},
#     {'id':2, 'name':'100 Days of Code'},
#     {'id':3, 'name':'CI CD in one shot'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    # Get username and password
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check if the user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # logins the user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is not correct!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                # simultaneously login the user
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'An Error occurred during Registraion')


    context = {'form':form}
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

    # For recent activity
    room_messages = Message.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)  # {'how to address in template':what to pass}
    

def room(request, pk):
    room = Room.objects.get(id=pk)
    # `message_set`queries sets of all messages related to Room (parent model)
    room_messages = room.message_set.all().order_by('-created')
    # To get all the participants
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        # To add user in the participants section
        return redirect('room', pk=room.id)


    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # `instance` is so that the form we get is pre filled
    form = RoomForm(instance=room)

    # To prevent someone else from accessing other's room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')


    if request.method == 'POST':
        # `instance` here will replace the pre filled value
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # To prevent someone else from accessing other's room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # To prevent someone else from accessing other's room
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})