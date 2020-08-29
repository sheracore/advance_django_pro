# advance_django_pro
advance django project with TDD, Travis CI and flake8

#### In this project all admin, models, code handled in core app
### ModelSeializer VS serializer
#### The ModelSerializer class is the same as a regular Serializer class, except that:
* It will automatically generate a set of fields for you, based on the model.
* It will automatically generate validators for the serializer, such as unique_together validators.
* It includes simple default implementations of .create() and .update().
#### PUT VS PATCH
* In put your method, request should contain entire fields but in PATHCH you can provide just one changed fied like jast username or just name
