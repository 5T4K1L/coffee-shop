from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('orders/', consumers.OrderConsumer.as_asgi()),
    path('time/', consumers.TimeConsumer.as_asgi()),
    path('track-order/', consumers.TrackConsumer.as_asgi())
]
