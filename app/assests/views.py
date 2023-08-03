from .models import Alert, Asset
from .serializers import AlertSerializer, AssetSerializer, RuleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class AlertAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        alerts = Alert.objects.filter(user=user)
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class AssetsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        asset = Asset.objects.filter(user=user)
        serializer = AssetSerializer(asset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class RuleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
