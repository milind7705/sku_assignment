from django.db import models
from rest_framework import serializers


class Location(models.Model):
    """
    @summary: Location Model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta(object):
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        app_label = 'api_manager'
        db_table = 'location'

    def __unicode__(self):
        return self.name


class LocationSerializer(serializers.ModelSerializer):
    """
    @summary: Location serializer
    """
    class Meta(object):
        model = Location
        fields = ("id", "name", "description")
        depth = 1
