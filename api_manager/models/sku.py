from django.db import models
from rest_framework import serializers
from . import SubCategory


class SKU(models.Model):
    """
    @summary: SKU Model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    subcategory = models.ForeignKey(SubCategory)

    class Meta(object):
        verbose_name = "SKU"
        verbose_name_plural = "SKUs"
        app_label = 'api_manager'
        db_table = 'sku'

    def __unicode__(self):
        return self.name


class SKUSerializer(serializers.ModelSerializer):
    """
    @summary: SKU Serializer
    """
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source='subcategory',
        write_only=True)

    class Meta(object):
        model = SKU
        fields = ("id", "name", "subcategory", "subcategory_id")
        depth = 4
