from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from petsapi.models import Pet, Animal_Type
from django.contrib.auth.models import User


class AnimalTypeView(ViewSet):
    def list(self, request):
        animal_types = Animal_Type.objects.all()
        serializer = AnimalTypeSerializer(
            animal_types, many=True, context={'request': request})
        return Response(serializer.data)
class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal_Type
        fields = ('name','id')