"""View module for handling requests about musicians"""
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gigtaxapi.models import Musician

class MusicianView(ViewSet):
    """Practice Plan Musicians"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single musician
        Returns:
            Response -- JSON serialized musician instance
        """
        try:

            musician = Musician.objects.get(pk=pk)
            serializer = MusicianSerializer(musician, context={'request': request})
            return Response(serializer.data)

        except Musician.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to categories resource
        Returns:
            Response -- JSON serialized list of categories
        """
        musicians = Musician.objects.all()

        serializer = MusicianSerializer(
            musicians, many=True, context={'request': request})
        return Response(serializer.data)
        

class MusicianSerializer(serializers.ModelSerializer):
    """JSON serializer for musicians

    Arguments:
        serializer type
    """
    class Meta:
        model = Musician
        fields = ('id', 'user', 'address')
        depth = 1