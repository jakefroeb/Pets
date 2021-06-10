from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from petsapi.models import Pet, Animal_Type
from django.contrib.auth.models import User


class PetView(ViewSet):
    def create(self, request):
        user=request.auth.user
        pet = Pet()
        animal_type = Animal_Type.objects.get(pk=request.data['animal'])
        pet.name = request.data["name"]
        pet.user = user
        pet.animal_type = animal_type
        try:
            pet.save()
            serializer = PetSerializer(many=False, context={'request':request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            pet = Pet.objects.get(pk=pk)
            serializer = PetSerializer(pet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        user = request.auth.user
        pets = Pet.objects.filter(user=user)
        serializer = PetSerializer(
            pets, many=True, context={'request': request})
        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal_Type
        fields = ('name','id')
class PetSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    animal_type = AnimalTypeSerializer(many=False)
    class Meta:
        model = Pet
        fields = ('id', 'name','user','animal_type')