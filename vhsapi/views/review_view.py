from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from vhsapi.models import Review, RareUser

class UserSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'user_full_name']
    
    def get_user_full_name(self, user):
        return user.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user.user', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'comment', 'user_info', 'movie', 'date_reviewed')

class ReviewView(viewsets.ViewSet):

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                review.content = serializer.validated_data['content']
                review.save()
                serializer = ReviewSerializer(review, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        reviews = Review.objects.all().order_by('date_reviewed')
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """
        try:
            review = Review.objects.get(pk=pk)
            serialized = ReviewSerializer(review)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def create(self, request):

        serialized = ReviewSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save(user=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED) 
        
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)

            if request.user.id != review.user_id:
                raise PermissionDenied("You do not have permission to delete this comment.")
            
            review.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def new_reviews(self, request):
        new_reviews = Review.objects.filter(user=request.user)
        serialized = ReviewSerializer(new_reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)