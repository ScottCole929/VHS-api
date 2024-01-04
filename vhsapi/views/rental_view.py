from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from vhsapi.models import RareUser, Rental, Movie
from django.db.utils import IntegrityError


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'cover_img_url', 'id',)


class RentalSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=False)

    class Meta:
        model = Rental
        fields = ('id', 'is_selected', 'is_active', 'date_rented', 'date_returned', 'returned_yet', 'movie', 'user',)



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

        movie_id = request.data.get('movie')

        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Could not find movie"}, status=status.HTTP_404_NOT_FOUND)
        
        is_active = request.data.get('is_active')
        is_selected = request.data.get('is_selected')

        try:
            rare_user = RareUser.objects.get(user=request.user)
        except RareUser.DoesNotExist:
            return Response({"error": "RareUser not found for auth user"}, status=status.HTTP_404_NOT_FOUND)

        already_selected = Rental.objects.filter(user=rare_user, is_selected=True).first()
        if already_selected:
            return Response({"error": "Only one tape can be selected at a time"}, status=status.HTTP_400_BAD_REQUEST)

        new_tape_rental = Rental.objects.create(
            user=rare_user,
            movie=movie,
            is_active=is_active,
            is_selected=is_selected,
        )
        
        serialized = RentalSerializer(new_tape_rental)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
        
    def update(self, request, pk=None):
        try:
            rental = Rental.objects.get(pk=pk)
            serialized = RentalSerializer(rental, data=request.data, partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rental.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    @action(methods=['get'], detail=False)
    def tape_selection(self, request):
        try:
            rare_user = RareUser.objects.get(user=request.user)
            current_choice = Rental.objects.filter(user=rare_user, is_active=False, is_selected=True).first()
            if current_choice:
                serialized = RentalSerializer(current_choice)
                return Response(serialized.data)
            return Response({"message": "No tape selected"}, status=status.HTTP_404_NOT_FOUND)
        except RareUser.DoesNotExist:
            return Response({"error": "RareUser not found"}, status=status.HTTP_404_NOT_FOUND)
    

    @action(methods=['get'], detail=False)
    def past_tape_rentals(self, request):
        rare_user = RareUser.objects.get(user=request.user)

        past_tape_rentals = Rental.objects.filter(user=rare_user, is_active=True)
        serialized = RentalSerializer(past_tape_rentals, many=True)
        return Response(serialized.data)
    

    @action(methods=['delete'], detail=True, url_path='remove-selected-tape')
    def remove_selected_tape(self, request, pk=None):
        print("Removing selected tape, ID:", pk)

        try:
            rare_user = RareUser.objects.get(user=request.user)
            rented_tape = Rental.objects.get(pk=pk, user=rare_user)
            if not rented_tape.is_selected:
                return Response({"error": "No tape selected at the moment"}, status=status.HTTP_400_BAD_REQUEST)
            
            rented_tape.is_selected = False
            rented_tape.save()
            return Response({"message": "Tape has been removed from your selection"}, status=status.HTTP_200_OK)
        
        except Rental.DoesNotExist:
            return Response({"error": "No rental was found"}, status=status.HTTP_404_NOT_FOUND)
    
        except Exception as event:
            return Response({"error": str(event)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['put'], url_path='rent-tape/(?P<rental_id>\d+)')
    def rent_tape(self, request, rental_id=None):
        try:
            rental = Rental.objects.get(pk=rental_id)
            rental.is_active = True
            rental.is_selected = True
            rental.save()

            serialized = RentalSerializer(rental)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Rental.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)