from django.urls import path

from ..apis import (
    AuthTokenView,
)
urlpatterns = [
    path('auth-token/', AuthTokenView.as_view()),
]