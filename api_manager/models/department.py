from django.db import models
from rest_framework import serializers

from . import Location


class Department(models.Model):
    """
    @summary: Department Model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location)

    class Meta(object):
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        app_label = 'api_manager'
        db_table = 'department'

    def __unicode__(self):
        return self.name


class DepartmentSerializer(serializers.ModelSerializer):
    """
    @summary: Department Serializer
    """
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True)

    class Meta(object):
        model = Department
        fields = ("id", "name", "description", "location", "location_id")
        depth = 2
