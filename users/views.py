from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        tg_chat_id = validated_data.get("tg_chat_id")

        user = User(email=email, tg_chat_id=tg_chat_id)
        user.set_password(password)
        user.save()

        serializer.instance = user
