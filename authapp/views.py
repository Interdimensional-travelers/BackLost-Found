from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer