from django.urls import path, include
from .views import PostView, Public, UsersView, Who_Am_I
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

urlpatterns = [
    path('public/', Public.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('whoami/', Who_Am_I.as_view()),
]

router = routers.SimpleRouter()
router.register(r'users', UsersView, basename="user")
router.register(r'posts', PostView, basename="post")
urlpatterns += router.urls
