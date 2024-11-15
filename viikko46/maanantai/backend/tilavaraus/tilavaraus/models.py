from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class KayttajaManager(BaseUserManager):
    def create_user(self, nimi, salasana, **extra_fields):
        if not nimi:
            raise ValueError('The Nimi field must be set')
        user = self.model(nimi=nimi, **extra_fields)
        user.set_password(salasana)
        user.save(using=self._db)
        return user

    def create_superuser(self, nimi, salasana, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nimi, salasana, **extra_fields)

class Kayttaja(AbstractBaseUser):
    tunnus = models.AutoField(primary_key=True)
    nimi = models.CharField(max_length=100, unique=True)
    rooli = models.CharField(max_length=10)  # 'user' or 'admin'
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Only required if using Admin

    objects = KayttajaManager()

    USERNAME_FIELD = 'nimi'  # Field for authentication
    REQUIRED_FIELDS = ['salasana']  # Fields required when creating a superuser

    class Meta:
        db_table = 'kayttaja'

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
