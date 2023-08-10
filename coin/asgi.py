import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coin.settings")

# coin 프로젝트의 ASGI 애플리케이션 가져오기
http_application = get_asgi_application()

# socket_channels 프로젝트의 WebSocket 라우터 생성
websocket_application = ProtocolTypeRouter(
    {
        "http": http_application,  # HTTP 프로토콜에 대한 애플리케이션 설정
        "websocket": URLRouter(websocket_urlpatterns),  # 웹 소켓 프로토콜에 대한 라우팅 설정
    }
)

# coin 프로젝트와 socket_channels 프로젝트를 합치는 최종 ASGI 애플리케이션

django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)