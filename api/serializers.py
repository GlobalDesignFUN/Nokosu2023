from rest_framework.serializers   import ModelSerializer
from .models import Info, Profile, User

class InfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__' 

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user