# Generated by Django 3.0.4 on 2020-03-28 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opsserver', '0006_auto_20200328_0058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipcount',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='ipcount',
            table='ip_count',
        ),
    ]