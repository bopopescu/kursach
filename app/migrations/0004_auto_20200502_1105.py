# Generated by Django 3.0.5 on 2020-05-02 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200429_1259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'permissions': (('full-service', 'Полный доступ к таблице услуг'), ('read-service', 'Чтение таблицы услуг'))},
        ),
    ]