from django.db import models
from django.utils import timezone
from rest_framework import serializers

# Create your models here.
class UserType(models.Model):
    """User type"""
    mtype = models.CharField(max_length=6, choices=(('1',"超级用户"),("2","普通用户")),default="2")
    def __str__(self):
        return self.username

    class Meta: 
        managed = True
        db_table = "user_type"


class User(models.Model):
    """User member"""
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    # user_type = models.ForeignKey("UserType", on_delete=models.CASCADE)
    user_type = models.CharField(max_length=6, choices=(('1',"超级用户"),("2","普通用户")),default="2")
    join_time = models.DateTimeField("加入时间", default=timezone.now)
    login_time = models.DateTimeField("最后登录时间", auto_now=True)
    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "user"
        ordering = ["-username"]

class UserSerializer(serializers.ModelSerializer):
    #username = serializers.CharField(max_length=30)
    #password = serializers.CharField(max_length=100)
    #email = serializers.EmailField()
    #user_type = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta: 
        model = User
        fields = ('username', 'password', 'email')

