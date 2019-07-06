from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack, AnonymousUser
from hello.consumers import send_data
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator



application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [ 
                     url(r"^playground/$",send_data)
                ]
            )
        )
    )
})