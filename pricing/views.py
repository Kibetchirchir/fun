from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from pricing.models import Pricing
from pricing.serializers import PricingSerializer, CalculatePriceSerializer
from utils.redis import cache_get, cache_set, cache_delete
import json
from datetime import datetime


class PricingView(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_tarrifs(self, request):
        cached_data = cache_get("tarrifs")
        if cached_data:
            print("retrieved from cache")
            return Response(cached_data, status=status.HTTP_200_OK)

        tarrifs = self.queryset.all()
        print("retrieved from database")
        serializer = self.get_serializer(tarrifs, many=True)
        data = {"rates": serializer.data, "cached_at": datetime.now().isoformat()}


        cache_set("tarrifs", data, ex=60*60*24)

        return Response(data, status=status.HTTP_200_OK)
    def calculate_price(self, request):
        serializer = CalculatePriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        weight = serializer.validated_data['weight']
        zone = serializer.validated_data['zone']
        tarrif = self.queryset.filter(zone=zone, weight__lte=weight).order_by('weight').values('price').first()
        if not tarrif:
            return Response({"error": "No tarrif found for this weight and zone"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"price": tarrif.price}, status=status.HTTP_200_OK)
    
    def clear_tarrifs(self, request):
        cache_delete("tarrifs")
        return Response({"message": "Tarrifs cleared from cache"}, status=status.HTTP_200_OK)