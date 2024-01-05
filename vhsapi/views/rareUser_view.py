from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
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
    

    # def update(self, request):

    #     try:
    #         rare_user = RareUser.objects.get(pk=pk)

    #         rare_user.bio = request.data["bio"]
    #         rare_user.zip_code = request.date["zip_code"]
    #         rare_user.state = request.data["state"]
    #         rare_user.street_address = request.data["street_address"]
    #         rare_user.city = request.data["city"]

    #         rare_user.save()

    #         user = rare_user.user
    #         user.email = request.data["email"]
    #         user.first_name = request.data["first_name"]
    #         user.last_name = request.data["last_name"]
    #         user.save()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)
        
    #     except ObjectDoesNotExist:
    #         return Response({"message": "This user could not be found"}, status=status.HTTP_404_NOT_FOUND)
    #     except KeyError:
    #         return Response({"message": "Data is in incorrect format"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        # Get the authenticated user
        user = request.user

        # Get the RareUser instance
        try:
            rare_user = RareUser.objects.get(user=user)
        except RareUser.DoesNotExist:
            return Response({"error": "RareUser not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the request is trying to update the correct profile
        if pk != str(rare_user.id):
            raise PermissionDenied("Cannot update another user's profile.")

        # Perform the update with request data
        serializer = RareUserSerializer(rare_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):

        try:
            rare_user = RareUser.objects.get(user=request.user)
            serialized = RareUserSerializer(rare_user)
            return Response(serialized.data)
        except RareUser.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


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
        fields = ('id', 'street_address', 'city', 'state', 'zip_code', 'bio', 'profile_img_url', 'created_on', 'active', 'user')



