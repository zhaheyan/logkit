# Generated by Django 3.0.4 on 2020-03-24 22:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(choices=[('1', '超级用户'), ('2', '普通用户')], default='2', max_length=6)),
                ('join_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='加入时间')),
                ('login_time', models.DateTimeField(auto_now=True, verbose_name='最后登录时间')),
            ],
            options={
                'db_table': 'user',
                'ordering': ['-username'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.CharField(choices=[('1', '超级用户'), ('2', '普通用户')], default='2', max_length=6)),
            ],
            options={
                'db_table': 'user_type',
                'managed': True,
            },
        ),
    ]
