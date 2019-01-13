from django.db import models
from rest_framework import serializers

from . import Department


class Category(models.Model):
    """
    @summary: Category Model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department)

    class Meta(object):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        app_label = 'api_manager'
        db_table = 'category'

    def __unicode__(self):
        return self.name


class CategorySerializer(serializers.ModelSerializer):
    """
    @summary: Category Serializer
    """
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department',
        write_only=True)

    class Meta(object):
        model = Category
        fields = ("id", "name", "description", "department", "department_id")
        depth = 3
