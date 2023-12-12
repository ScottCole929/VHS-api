from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vhsapi.models import Movie
from django.core.exceptions import PermissionDenied


class MovieSerializer(serializers.ModelSerializer):
    """JSON serializer for types"""
    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_year', 'starring', 'director', 'genre', 'production_studio', 'cover_img_url', 'is_available')

class MovieView(ViewSet):
    def list(self, request):
        """Handle GET requests to get all Categories
        
        Returns:
            response -- JSON serialized list of types
        """

        movies = Movie.objects.all().order_by('title')
        serialized = MovieSerializer(movies, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            single_movie = Movie.objects.get(pk=pk)
            serialized = MovieSerializer(single_movie)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)