from rest_framework import serializers
from .models import Kayttaja, Tilat, Varaajat, Varaukset

class KayttajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kayttaja
        fields = ['tunnus', 'nimi', 'salasana']

class TilatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tilat
        fields = ['id', 'tilan_nimi']

class VaraajatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varaajat
        fields = ['id', 'nimi']

class VarauksetSerializer(serializers.ModelSerializer):
    tila = TilatSerializer(read_only=True)
    varaaja = VaraajatSerializer(read_only=True)

    class Meta:
        model = Varaukset
        fields = ['id', 'tila', 'varaaja', 'varauspaiva']

