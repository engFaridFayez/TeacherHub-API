from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.views import APIView, Response
from users.models import CustomUser
from users.serializers import ProfileSerializer, RegisterSerializer
# Create your views here.


class Register(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class Me(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        serializer = ProfileSerializer(request.user,context={"request":request})
        return Response(serializer.data)
