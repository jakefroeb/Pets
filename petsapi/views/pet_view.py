from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from petsapi.models import Pet, Animal_Type, Action, Pet_Action
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action

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

    def destroy(self, request, pk=None):
        try:
            pet = Pet.objects.get(pk=pk)
            pet.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Pet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        user = request.auth.user
        pets = Pet.objects.filter(user=user)
        for pet in pets:
            print(pet.happiness)
        serializer = PetSerializer(
            pets, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True)
    def interact(self, request, pk=None):
        if request.method == "POST":
            try:
                user = request.auth.user
                pet_action = Pet_Action()
                pet = Pet.objects.get(pk=pk, user=user)
                action = Action.objects.get(pk=request.data["action"])
                pet_action.pet = pet
                pet_action.action = action
                pet_action.save()
                return Response({}, status=status.HTTP_201_CREATED)
            except Pet.DoesNotExist as ex:
                return Response({'Pet could not be found': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            except Action.DoesNotExist as ex:
                return Response({'Action could not be found': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('name','id')
class AnimalTypeSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)
    class Meta:
        model = Animal_Type
        fields = ('name','id', 'actions')
class PetSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    animal_type = AnimalTypeSerializer(many=False)
    class Meta:
        model = Pet
        fields = ('id', 'name','user','animal_type','happiness', 'image_url')