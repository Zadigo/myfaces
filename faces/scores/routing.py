from django.urls import re_path
from scores import consumers

websocket_urlpatterns = [
    re_path(
        r'^ws/session$',
        consumers.FaceConsumer.as_asgi()
    )
]
