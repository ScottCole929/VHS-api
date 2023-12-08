from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vhsapi.models import Genre

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for types"""
    class Meta:
        model = Genre
        fields = ('id', 'label', )

class GenreView(ViewSet):
    def list(self, request):
        """Handle GET requests to get all Categories
        
        Returns:
            response -- JSON serialized list of types
        """
        genres = Genre.objects.all().order_by('label')
        serialized = GenreSerializer(genres, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            single_genre = Genre.objects.get(pk=pk)
            serialized = GenreSerializer(single_genre)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        genre = Genre()
        genre.label = request.data['label']
        genre.save()

        serialized = GenreSerializer(genre, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(data=request.data)
            if serializer.is_valid():
                genre.label = serializer.validated_data['label']
                genre.save()
                serializer = GenreSerializer(genre, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            genre.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
