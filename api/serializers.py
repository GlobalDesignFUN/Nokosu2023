from rest_framework.serializers import ModelSerializer
from .models import Info, Profile

class InfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__' 

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 