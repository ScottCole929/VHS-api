from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from vhsapi.models import Review, RareUser, Movie

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'cover_img_url', 'id',)

class UserSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'user_full_name']
    
    def get_user_full_name(self, user):
        return user.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user.user', read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True, source='movie')
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'comment', 'user_info', 'movie', 'date_reviewed', 'movie_id')

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

class ReviewView(viewsets.ViewSet):

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            
            if review.user.user != request.user:
                return Response({"error": "You are not allowed to edit this post"}, status=status.HTTP_403_FORBIDDEN)
        
            serialized = ReviewSerializer(review, data=request.data, partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors, status.HTTP_400_BAD_REQUEST)

        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        reviews = Review.objects.all().order_by('date_reviewed')
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            serialized = ReviewSerializer(review)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    
    def create(self, request):
        rare_user = RareUser.objects.get(user=request.user)

        movie_id = int(request.data.get('movie'))

        try:
            movie_example = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        review_example = Review(
            title=request.data.get('title'),
            comment=request.data.get('comment'),
            user=rare_user,
            movie=movie_example
        )

        review_example.save()
        return Response(ReviewSerializer(review_example).data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)

            if request.user != review.user.user:
                raise PermissionDenied("You do not have permission to delete this comment.")
            
            review.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def new_reviews(self, request):
        new_reviews = Review.objects.filter(user=request.user)
        serialized = ReviewSerializer(new_reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        rare_user = RareUser.objects.get(user=request.user)
        user_reviews = Review.objects.filter(user=rare_user)

        serialized = ReviewSerializer(user_reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
