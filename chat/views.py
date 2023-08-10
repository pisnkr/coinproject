from django.shortcuts import render, redirect
from .models import ChatRoom
from .forms import ChatRoomForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='common:login')  # 로그인된 사용자만 접근 가능
def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        chat_room = ChatRoom.objects.create(name=room_name)
        return redirect('chat:index')
    return redirect('chat:index')

@login_required(login_url='common:login')  # 로그인된 사용자만 접근 가능
def index(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'chat_rooms': chat_rooms})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/chat_rooms.html', {'chat_rooms': chat_rooms})
