from django.db import models
from rest_framework import serializers

from . import Category


class SubCategory(models.Model):
    """
    @summary: SubCategory Model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category)

    class Meta(object):
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        app_label = 'api_manager'
        db_table = 'subcategory'

    def __unicode__(self):
        return self.name


class SubCategorySerializer(serializers.ModelSerializer):
    """
    @summary: SubCategory Serializer
    """
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "name", "description", "category", "category_id")
        depth = 3
