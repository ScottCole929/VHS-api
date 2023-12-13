from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vhsapi.models import Movie, MovieGenre
from .genre_view import GenreSerializer
from django.core.exceptions import PermissionDenied


class MovieSerializer(serializers.ModelSerializer):
    genre_data = serializers.SerializerMethodField()
    """JSON serializer for types"""
    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_year', 'starring', 'director', 'genre_data', 'production_studio', 'cover_img_url', 'is_available')

    def get_genre_data(self, movie):
        genre_name = movie.genre.all()
        return GenreSerializer(genre_name, many=True).data


    def create(self, correct_data):
        genre_nums = correct_data.pop('genre_nums', [])
        movie = Movie.objects.create(**correct_data)

        for genre_num in genre_nums:
            MovieGenre.objects.create(movie=movie, genre_num=genre_num)

        return movie

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
        

    def create(self, request):

        serialized = MovieSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)