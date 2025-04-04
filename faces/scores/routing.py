from scores import consumers
from django.urls import path, re_path

websocket_urlpatterns = [
    re_path(
        r'^ws/session$',
        consumers.FaceConsumer.as_asgi()
    )
]
