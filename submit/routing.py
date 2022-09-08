from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('submit/ws', consumers.SubmitConsumer.as_asgi())
]
