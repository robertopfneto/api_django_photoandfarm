from rest_framework import serializers
from .models import Farm, Person, Photo

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name', 'rua','numero','bairro']



class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'cpf', 'fk_farm']
        read_only_fields = ['fk_farm']

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = Photo
        fields = ['id', 'name', 'created_at', 'image', 'fk_farm', 'fk_person']
        read_only_fields = ['fk_farm', 'fk_person']