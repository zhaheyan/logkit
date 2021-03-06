# Generated by Django 3.0.4 on 2020-03-24 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('agent_ip', models.CharField(blank=True, max_length=16)),
                ('agent_status', models.CharField(choices=[('health', '正常'), ('abnormal', '异常')], max_length=8)),
                ('management', models.CharField(blank=True, max_length=16, null=True)),
                ('operation', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'db_table': 'agent',
                'managed': True,
            },
        ),
    ]
