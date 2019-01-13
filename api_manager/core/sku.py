from rest_framework import HTTP_HEADER_ENCODING, exceptions, status, response
from api_manager.models import SubCategory, SubCategorySerializer, \
    SKU, SKUSerializer

REQUIRED_PARAMS = ['location', 'department', 'category', 'subcategory']


def get_sku_by_filters(request):
    try:
        params = request.query_params
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
