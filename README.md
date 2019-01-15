# README #

SKU assignment for the problem statement provided.

# Changes #
Solved all the problems except the UI ones.
1. Implementated API authentication(basic)
2. Implemented all the APIs functionalities
3. Checked in all the models and their serializers
4. Implemented Swagger for the apis
5. Added schema.PNG for the assignment schema

## Unit Testing ##
Unit testing for one API is done.

[root@6fded22b4c5b sku_assignment]# python manage.py test unit_tests/test_sku.py --verbosity=2

nosetests unit_tests/test_sku.py --verbosity=2
@summary: Unit test for sku api with invalid parameters ... ok
@summary: Unit test for sku api with exception ... ok
@summary: Unit test for sku api with success ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.047s

OK


Steps to setup and execute:
1. Setup a virtual environment
2. Execute pip install -r requirements.txt
3. Create the DB in mysql and add it to the settings.py along with ports
4. Execute "python manage.py runserver 0.0.0.0:80"
