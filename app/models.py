from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db import models

# Create your models here.
#@admin.register()

class client(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    FIO = models.CharField(max_length=255)
    addres = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    balance = models.DecimalField(decimal_places=2, max_digits=8)
    class Meta:
        permissions = (
            ('full-client', 'Изменение, чтение, добавление клиентов'),
            ('limited-client', 'Чтение всей информации и изменение номера телефона и баланса')
        )


class service(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    service_name = models.CharField(max_length=30)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    tarif_type = models.CharField(max_length=20)
    class Meta:
        permissions = (
            ('full-service', "Полный доступ к таблице услуг"),
            ('read-service', 'Чтение таблицы услуг')
        )

class provider(models.Model):
   id = models.AutoField(primary_key=True, db_index=True)
   provider_name = models.CharField(max_length=255)
   provide_service = models.ForeignKey(service,on_delete=models.CASCADE)
   class Meta:
        permissions = (
            ('full-provider', 'Полный доступ к таблице поставщиков'),
        )


class rendered_service(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    id_client = models.ForeignKey(client, on_delete=models.CASCADE)
    id_service = models.ForeignKey(service, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=8)
    class Meta:
        permissions = (
            ('create-rendered-service', 'Создвние новой оказаннной услуги'),
            ('read-rendered-service', 'Чтение оказанных услуг'),
            ('full-rendered-service', 'Полный доступ к оказанным услугам')
        )

class provided_service(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    date = models.DateTimeField()
    provider = models.ForeignKey(provider, on_delete=models.CASCADE)
    service = models.ForeignKey(service, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=8)
    class Meta:
        permissions = (
            ('full-provided-service', 'Полный доступ к поставленным услугам'),
        )