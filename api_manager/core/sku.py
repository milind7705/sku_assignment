from rest_framework import status, response
from api_manager.models import SubCategory, SubCategorySerializer, \
    SKU, SKUSerializer
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from functools import wraps

REQUIRED_PARAMS = ['location', 'department', 'category', 'subcategory']


def get_sku_by_filters(request):
    """
    @summary: A function to fetch the skus
    @param request (object): request object
    @return sku: response object
    """
    try:
        params = request.query_params
        if not params:
            params = request.data
        missing_params = set(REQUIRED_PARAMS) - set(params)
        if missing_params:
            message = "Input parameter missing for the api: {}".\
                format(",".join(missing_params))
            return response.Response(status=status.HTTP_400_BAD_REQUEST,
                                     data=message)
        subcategory = params.get("subcategory")
        category = params.get("category")
        department = params.get("department")
        location = params.get("location")
        subcategories = SubCategorySerializer(SubCategory.objects.filter(
            name=subcategory), many=True).data

        sku_list = []
        for each_subcategory in subcategories:
            if each_subcategory.get('name') == subcategory \
                    and each_subcategory.get('category').\
                            get('name') == category \
                    and each_subcategory.get('category').get('department').\
                    get('name') == department and \
                    each_subcategory.get('category').\
                    get('department').get('location').get('name') == location:
                sku_list = SKUSerializer(SKU.objects.filter(
                    subcategory=each_subcategory.get('id')),many=True).data
                for sku in sku_list:
                    subcategory_dict = sku.pop('subcategory')
                    category_dict = subcategory_dict.pop('category')
                    department_dict = category_dict.pop('department')
                    location_dict = department_dict.pop('location')
                    sku.update({'subcategory': subcategory_dict.get("name"),
                                'category': category_dict.get("name"),
                                'department': department_dict.get("name"),
                                'location': location_dict.get("name")})
        return response.Response(status=status.HTTP_200_OK, data=sku_list)
    except Exception as e:
        return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 data=e.message)


def get_skus_by_body(request):
    """
    @summary: A function to fetch the skus
    @param request (object): request object
    @return sku: response object
    """
    return get_sku_by_filters(request)


def body(schema=None):
    """
    @summary: A decorator to perform schema validation
    @param dict: json schema
    """
    def function_wrapper(func):
        @wraps(func)
        def returned_wrapper(request):
            try:
                json_params = request.data if request.data else {}
                validate(json_params, schema)
            except ValidationError as err:
                return response.Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=err.message)
            return func(request)
        return returned_wrapper
    return function_wrapper
