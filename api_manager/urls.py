from django.conf.urls import url
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views import LocationViewSet, DepartmentViewSet, CategoryViewSet, \
    SubCategoryViewSet, get_sku_by_params, schema_view, login, get_skus, logout


router = ExtendedSimpleRouter()

location_router = router.register(
    r'locations', LocationViewSet, base_name='location')
department_router = location_router.register(
    r'departments', DepartmentViewSet, base_name='location-departments',
    parents_query_lookups=['location'])
category_router = department_router.register(
    r'categories', CategoryViewSet,
    base_name='location-departments-categories',
    parents_query_lookups=['department__location',
                           'department'])
sub_category_router = category_router.register(
    r'subcategories', SubCategoryViewSet, base_name='organizations-group',
    parents_query_lookups=['category__department__location',
                           'category__department',
                           'category'])

urlpatterns = [
    url(r'^$', schema_view), # swagger URLS
    url(r'^sku/', get_sku_by_params, name="sku"),# the sku api
    url(r'login/', login, name='login'),
    url(r'logout/', logout, name='logout'),
    url(r'^skus/', get_skus, name="skus")
]

urlpatterns += router.urls
