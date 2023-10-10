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
        fields = ('id',
                  'username',
                  'password',
                  'email',
                  'first_name',
                  'last_name',
                  'is_active',
                  'is_staff',
                  'is_superuser',
                  'date_joined',
                  'last_login',
                )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        filtered_data = {'username': validated_data['username'],
                        'password': validated_data['password'],
                        'email': validated_data['email'],
                        'first_name': validated_data['first_name'],
                        'last_name': validated_data['last_name'],
                        }
        user = User.objects.create_user(**filtered_data)
        return user
    
    def update(self, user, validated_data):
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user
    