
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),  # 처음 메인 화면 뷰
    path('chat_rooms/', views.chat_rooms, name='chat_rooms'),  # 채팅방 목록 뷰
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),  # 새 채팅방 생성 뷰
    path('<str:room_name>/', views.room, name='room'),  # 채팅방 뷰
    
]