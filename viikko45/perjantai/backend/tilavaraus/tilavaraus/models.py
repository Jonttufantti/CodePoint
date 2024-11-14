from django.db import models

class Kayttaja(models.Model):
    tunnus = models.AutoField(primary_key=True)
    nimi = models.CharField(max_length=100)
    salasana = models.CharField(max_length=100)

    class Meta:
        db_table = 'kayttajat'

    def __str__(self):
        return self.nimi


class Tilat(models.Model):
    id = models.AutoField(primary_key=True)
    tilan_nimi = models.CharField(max_length=16)

    class Meta:
        db_table = 'tilat'

    def __str__(self):
        return self.tilan_nimi


class Varaajat(models.Model):
    id = models.AutoField(primary_key=True)
    nimi = models.CharField(max_length=64)

    class Meta:
        db_table = 'varaajat'

    def __str__(self):
        return self.nimi


class Varaukset(models.Model):
    id = models.AutoField(primary_key=True)
    tila = models.ForeignKey(Tilat, on_delete=models.CASCADE)
    varaaja = models.ForeignKey(Varaajat, on_delete=models.CASCADE)
    varauspaiva = models.DateField()

    class Meta:
        db_table = 'varaukset'

    def __str__(self):
        return f"{self.varauspaiva} - {self.tila} by {self.varaaja}"
