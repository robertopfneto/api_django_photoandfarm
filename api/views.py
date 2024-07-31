from django.http import Http404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from .models import Farm, Person, Photo
from .serializers import FarmSerializer, PersonSerializer, PhotoSerializer

class FarmList(ListAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

class FarmDetail(APIView):
    def get_object(self, pk):
        try:
            return Farm.objects.get(pk=pk)
        except Farm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        farm = self.get_object(pk)
        serializer = FarmSerializer(farm)
        return Response(serializer.data)

class PersonList(ListAPIView):
    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonSerializer

class PersonDetail(APIView):
    def get_object(self, name):
        try:
            return Person.objects.get(name=name)
        except Person.DoesNotExist:
            raise Http404("Pessoa não encontrada")

    def get(self, request, name, format=None):
        person = self.get_object(name)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

class PhotoList(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class CreateUpdatePhoto(APIView):
    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            farm_id = request.data.get('fk_farm', None)
            person_id = request.data.get('fk_person', None)

            # Salvar a foto e associar as chaves estrangeiras
            photo_instance = serializer.save(fk_farm_id=farm_id, fk_person_id=person_id)

            if photo_instance:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Falha ao salvar foto'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateFarm(CreateAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def perform_create(self, serializer):
        rua = self.request.data.get('rua')
        numero = self.request.data.get('numero')
        bairro = self.request.data.get('bairro')

        # Verifica se já existe uma fazenda com os mesmos valores de rua, numero e bairro

        if Farm.objects.filter(rua=rua, numero=numero, bairro=bairro).exists():
            raise serializers.ValidationError("Já existe uma fazenda cadastrada com esses dados.")

        # Se não houver nenhuma fazenda com os mesmos valores, cria a nova instância
        serializer.save()

class CreatePerson(CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def create(self, request, *args, **kwargs):
        person_data = request.data
        farm_id = person_data.pop('fk_farm', None)

        # Verifica se o CPF já está cadastrado
        cpf = person_data.get('cpf', None)
        if cpf and Person.objects.filter(cpf=cpf).exists():
            return Response({'error': 'Pessoa com CPF já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)

        # Cria a pessoa sem associar a fazenda primeiro
        person_serializer = self.get_serializer(data=person_data)
        if person_serializer.is_valid():
            person_instance = person_serializer.save()

            # Se existir ID da fazenda, tenta associar a pessoa à fazenda correspondente
            if farm_id:
                try:
                    farm = Farm.objects.get(id=farm_id)
                    person_instance.fk_farm = farm
                    person_instance.save()
                except Farm.DoesNotExist:
                    # Remove a pessoa criada se a fazenda não existir
                    person_instance.delete()
                    return Response({'error': 'Fazenda não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(person_serializer.data, status=status.HTTP_201_CREATED)
        return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
