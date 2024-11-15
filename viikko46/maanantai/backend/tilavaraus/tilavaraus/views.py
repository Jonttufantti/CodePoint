from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Kayttaja, Tilat, Varaajat, Varaukset
from .serializers import KayttajaSerializer, TilatSerializer, VaraajatSerializer, VarauksetSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser, IsUserOrReadOnly

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrReadOnly])
def kayttaja_list(request):
    if request.method == 'GET':
        kayttajat = Kayttaja.objects.all()
        serializer = KayttajaSerializer(kayttajat, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = KayttajaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def kayttaja_detail(request, pk):
    try:
        kayttaja = Kayttaja.objects.get(pk=pk)
    except Kayttaja.DoesNotExist:
        return Response({'Error': 'Kayttaja not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KayttajaSerializer(kayttaja)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = KayttajaSerializer(kayttaja, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        kayttaja.delete()
        return Response({'message': 'Kayttaja deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrReadOnly])
def tilat_list(request):
    if request.method == 'GET':
        tilat = Tilat.objects.all()
        serializer = TilatSerializer(tilat, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TilatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def tilat_detail(request, pk):
    try:
        tila = Tilat.objects.get(pk=pk)
    except Tilat.DoesNotExist:
        return Response({'Error': 'Tila not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TilatSerializer(tila)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TilatSerializer(tila, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tila.delete()
        return Response({'message': 'Tila deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrReadOnly])
def varaajat_list(request):
    if request.method == 'GET':
        varaajat = Varaajat.objects.all()
        serializer = VaraajatSerializer(varaajat, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VaraajatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def varaajat_detail(request, pk):
    try:
        varaaja = Varaajat.objects.get(pk=pk)
    except Varaajat.DoesNotExist:
        return Response({'Error': 'Varaaja not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VaraajatSerializer(varaaja)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VaraajatSerializer(varaaja, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        varaaja.delete()
        return Response({'message': 'Varaaja deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrReadOnly])
def varaukset_list(request):
    if request.method == 'GET':
        varaukset = Varaukset.objects.all()
        serializer = VarauksetSerializer(varaukset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VarauksetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def varaukset_detail(request, pk):
    try:
        varaus = Varaukset.objects.get(pk=pk)
    except Varaukset.DoesNotExist:
        return Response({'Error': 'Varaus not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VarauksetSerializer(varaus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VarauksetSerializer(varaus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        varaus.delete()
        return Response({'message': 'Varaus deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
