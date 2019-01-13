from django.http import HttpResponse
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Location, LocationSerializer, Department, \
    DepartmentSerializer, Category, CategorySerializer, \
    SubCategory, SubCategorySerializer
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes, \
    permission_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.permissions import AllowAny
import urls
from core.sku import get_sku_by_filters
from core.authorization import get_login_credentials
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    @summary: login view
    @param request object
    @return Response(Response object): token response
    """
    username, password = get_login_credentials(request)
    if not (username and password):
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class MyViewSet(NestedViewSetMixin, CreateModelMixin, RetrieveModelMixin,
                DestroyModelMixin, ListModelMixin, GenericViewSet,
                UpdateModelMixin):
    """
    @summary: viewset for all the operations
    """
    pass


class LocationViewSet(MyViewSet):
    """
    @summary: viewset for location
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DepartmentViewSet(MyViewSet):
    """
    @summary: viewset for department
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CategoryViewSet(MyViewSet):
    """
    @summary: viewset for category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(MyViewSet):
    """
    @summary: viewset for subcategory
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


@api_view(['GET'])
def get_sku_by_params(request):
    """
    @summary: viewset for location
    @param request object
    @return Response(Response object): sku response
    """
    return get_sku_by_filters(request)


# swagger documentation
@api_view()
@permission_classes((AllowAny,))
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    """
    @summary: view for swagger
    @param request object
    @return Response(Response object): swagger response
    """
    generator = schemas.SchemaGenerator(title='SKU API Documentation',
                                        patterns=urls.urlpatterns,
                                        url="/api/v1/")
    return response.Response(generator.get_schema(request=request))