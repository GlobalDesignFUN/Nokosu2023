from rest_framework.serializers import ModelSerializer
from .models import Info, Location, Profile

class InfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__' 

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__' 