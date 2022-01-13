"""View module for handling requests about tours"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gigtaxapi.models import Tour, Musician
from django.db.models import Q

class TourView(ViewSet):
    """Gig Tax Tours"""

    def create(self, request):
        """Handle POST operations for a tour
        Returns:
            Response -- JSON serialized tour instance
        """
        musician = Musician.objects.get(user=request.auth.user)

        tour = Tour()
        tour.musician = musician
        tour.artist = request.data["artist"]
        tour.tour_departure_address = request.data["tourDepartureAddress"]
        tour.tour_description = request.data["tourDescription"]
        tour.number_of_gigs = request.data["numberOfGigs"]
        tour.per_diem = request.data["perDiem"]
        tour.travel_days = request.data["travelDays"]
        tour.travel_day_pay = request.data["travelDayPay"]
        tour.date_start = request.data["dateStart"]
        tour.date_end = request.data["dateEnd"]
        tour.tour_gig_pay = request.data["tourGigPay"]
        tour.mileage = request.data["mileage"]

        try:
            tour.save()
            serializer = TourSerializer(tour, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tour

        Returns:
            Response -- JSON serialized tour instance
        """
        try:
            # tour = Tour.objects.get(pk=pk)
            tour = Tour.objects.get(Q(pk=pk) & Q(musician__user=request.auth.user))
            serializer = TourSerializer(tour, context={'request': request})
            return Response(serializer.data)

        except Tour.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a tour

        Returns:
            Response -- Empty body with 204 status code
        """
        musician = Musician.objects.get(user=request.auth.user)

        tour = Tour.objects.get(pk=pk)
        tour.musician = musician
        tour.artist = request.data["artist"]
        tour.tour_departure_address = request.data["tourDepartureAddress"]
        tour.tour_description = request.data["tourDescription"]
        tour.number_of_gigs = request.data["numberOfGigs"]
        tour.per_diem = request.data["perDiem"]
        tour.travel_days = request.data["travelDays"]
        tour.travel_day_pay = request.data["travelDayPay"]
        tour.date_start = request.data["dateStart"]
        tour.date_end = request.data["dateEnd"]
        tour.tour_gig_pay = request.data["tourGigPay"]
        tour.mileage = request.data["mileage"]
        tour.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tour
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tour = Tour.objects.get(pk=pk)
            tour.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tour.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to tours resource
        Returns:
            Response -- JSON serialized list of tours
        """
        tours = Tour.objects.filter(musician__user=request.auth.user)

        serializer = TourSerializer(
            tours, many=True, context={'request': request})
        return Response(serializer.data)

class TourSerializer(serializers.ModelSerializer):
    """JSON serializer for tours

    Arguments:
        serializer type
    """
    class Meta:
        model = Tour
        fields = ('__all__')
        depth = 2