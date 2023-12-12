from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from vhsapi.models import RareUser, Rental, Movie


class RentalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental
        fields = ('date_rented', 'date_returned', 'returned_yet', 'movie', 'user',)


class RentalView(viewsets.ViewSet):

    def list(self, request):
        rentals = Rental.objects.all().order_by('date_rented')
        serialized = RentalSerializer(rentals, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            rental = Rental.objects.get(pk=pk)
            serialized = RentalSerializer(rental)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Rental.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        serialized = RentalSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)