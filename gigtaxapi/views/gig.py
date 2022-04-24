"""View module for handling requests about gigs"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gigtaxapi.models import Gig, Musician
from django.db.models import Q

class GigView(ViewSet):
    """Gig Tax Gigs"""

    def create(self, request):
        """Handle POST operations for a gig
        Returns:
            Response -- JSON serialized gig instance
        """
        musician = Musician.objects.get(user=request.auth.user)

        gig = Gig()
        gig.musician = musician
        gig.artist = request.data["artist"]
        gig.location_name = request.data["locationName"]
        gig.location_address = request.data["locationAddress"]
        gig.gig_description = request.data["gigDescription"]
        gig.date = request.data["date"]
        gig.gig_pay = request.data["gigPay"]
        gig.mileage = request.data["mileage"]

        try:
            gig.save()
            serializer = GigSerializer(gig, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single gig

        Returns:
            Response -- JSON serialized gig instance
        """
        try:
            # gig = Gig.objects.get(pk=pk)
            gig = Gig.objects.get(Q(pk=pk) & Q(musician__user=request.auth.user))
            serializer = GigSerializer(gig, context={'request': request})
            return Response(serializer.data)

        except Gig.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a gig

        Returns:
            Response -- Empty body with 204 status code
        """
        musician = Musician.objects.get(user=request.auth.user)

        gig = Gig.objects.get(pk=pk)
        gig.musician = musician
        gig.artist = request.data["artist"]
        gig.location_name = request.data["locationName"]
        gig.location_address = request.data["locationAddress"]
        gig.gig_description = request.data["gigDescription"]
        gig.date = request.data["date"]
        gig.gig_pay = request.data["gigPay"]
        gig.mileage = request.data["mileage"]
        gig.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single gig
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            gig = Gig.objects.get(pk=pk)
            gig.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Gig.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to gigs resource
        Returns:
            Response -- JSON serialized list of gigs
        """
        gigs = Gig.objects.filter(musician__user=request.auth.user)

        serializer = GigSerializer(
            gigs, many=True, context={'request': request})
        return Response(serializer.data)

class GigSerializer(serializers.ModelSerializer):
    """JSON serializer for gigs

    Arguments:
        serializer type
    """
    class Meta:
        model = Gig
        fields = ('__all__')
        depth = 2