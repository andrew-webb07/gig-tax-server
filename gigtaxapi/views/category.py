"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gigtaxapi.models import Category

class CategoryView(ViewSet):
    """Gig Tax Categories"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to categorys resource

        Returns:
            Response -- JSON serialized list of categorys
        """

        categorys = Category.objects.all()

        serializer = CategorySerializer(
            categorys, many=True, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys

    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1
