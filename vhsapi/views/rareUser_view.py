"""View module for handling requests about rare_users"""
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from vhsapi.models import RareUser


class RareUserView(ViewSet):
    """Viewset for rare_users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        rare_user = RareUser.objects.get(pk=pk)
        serialized = RareUserSerializer(rare_user)
        return Response(serialized.data)


    def list(self, request):
        """Handle GET requests to rare_users resource

        Returns:
            Response -- JSON serialized list of rare_users
        """
        rare_user = RareUser.objects.all().order_by('rare_username')
        serialized = RareUserSerializer(rare_user, many=True)
        return Response(serialized.data)

class UserRareUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()

    def get_email(self, obj):
        return f'{obj.username}'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    def get_is_staff(self, obj):
        return f'{obj.is_staff}'

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'is_staff',)

class RareUserSerializer(serializers.ModelSerializer):
  
    user = UserRareUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'street_address', 'city', 'state', 'zip_code', 'bio', 'profile_image_url', 'created_on', 'active', 'user')
