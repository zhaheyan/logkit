from django.db import models
from rest_framework import serializers

# Create your models here.
class Agent(models.Model):
    """request data"""
    # id = models.IntegerField(primary_key=True, blank=True)a
    id = models.AutoField(primary_key=True)
    agent_ip = models.CharField(max_length=32, blank=True)
    agent_status = models.CharField(max_length=8, choices=(("health", "正常"), ("abnormal", "异常")))
    management = models.CharField(max_length=16, blank=True, null=True)
    operation = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        """RequestData meta data"""
        managed = True
        db_table = "agent"
        # ordering = ["-remote_addr"]

class AgentSerializer(serializers.Serializer):
    class Meta: 
        model = Agent
        fields = '__all__'

