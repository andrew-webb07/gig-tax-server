"""View module for handling requests about receipts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gigtaxapi.models import Receipt, Musician, Category
from django.db.models import Q

class ReceiptView(ViewSet):
    """Gig Tax Receipts"""

    def create(self, request):
        """Handle POST operations for a receipt
        Returns:
            Response -- JSON serialized receipt instance
        """
        musician = Musician.objects.get(user=request.auth.user)

        receipt = Receipt()
        receipt.musician = musician
        receipt.business_name = request.data["businessName"]
        receipt.business_address = request.data["businessAddress"]
        receipt.description = request.data["description"]
        receipt.date = request.data["date"]
        receipt.price = request.data["price"]
        receipt.receipt_number = request.data["receiptNumber"]

        receipt.category = Category.objects.get(pk=request.data["category"])

        try:
            receipt.save()
            serializer = ReceiptSerializer(receipt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single receipt

        Returns:
            Response -- JSON serialized receipt instance
        """
        try:
            # receipt = Receipt.objects.get(pk=pk)
            receipt = Receipt.objects.get(Q(pk=pk) & Q(musician__user=request.auth.user))
            serializer = ReceiptSerializer(receipt, context={'request': request})
            return Response(serializer.data)

        except Receipt.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a receipt

        Returns:
            Response -- Empty body with 204 status code
        """
        musician = Musician.objects.get(user=request.auth.user)

        receipt = Receipt.objects.get(pk=pk)
        receipt.musician = musician
        receipt.business_name = request.data["businessName"]
        receipt.business_address = request.data["businessAddress"]
        receipt.description = request.data["description"]
        receipt.date = request.data["date"]
        receipt.price = request.data["price"]
        receipt.receipt_number = request.data["receiptNumber"]
        receipt.category = Category.objects.get(pk=request.data["category"])
        receipt.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single receipt
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            receipt = Receipt.objects.get(pk=pk)
            receipt.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Receipt.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to receipts resource
        Returns:
            Response -- JSON serialized list of receipts
        """
        receipts = Receipt.objects.filter(musician__user=request.auth.user)

        serializer = ReceiptSerializer(
            receipts, many=True, context={'request': request})
        return Response(serializer.data)

class ReceiptSerializer(serializers.ModelSerializer):
    """JSON serializer for receipts

    Arguments:
        serializer type
    """
    class Meta:
        model = Receipt
        fields = ('__all__')
        depth = 2