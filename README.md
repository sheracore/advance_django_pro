# advance_django_pro
advance django project with TDD, Travis CI and flake8.
* This project have four apps contain app(core app), core, user, recipe that core has basic admin and all model and each recipe and user have its serializers, views, urls and tests.

#### In this project all admin, models, code handled in core app

### Using mixins
#### One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.
#### The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.
* So you can use mixin to customize CRUD methods.
```
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```
### ModelViewSet
#### The ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, by mixing in the behavior of the various mixin classes.
* The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().
* Because ModelViewSet extends GenericAPIView, you'll normally need to provide at least the queryset and serializer_class attributes. For example:
```
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```
#### Note that you can use any of the standard attributes or method overrides provided by GenericAPIView. For example, to use a ViewSet that dynamically determines the queryset it should operate on, you might do something like this:
```
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()
```

### ModelSeializer VS serializer
#### The ModelSerializer class is the same as a regular Serializer class, except that:
* It will automatically generate a set of fields for you, based on the model.
* It will automatically generate validators for the serializer, such as unique_together validators.
* It includes simple default implementations of .create() and .update().
#### PUT VS PATCH
* In put your method, request should contain entire fields but in PATHCH you can provide just one changed fied like jast username or just name

### ManyToMany relatoins

#### ManyToManyField accepts an extra set of arguments – all optional – that control how the relationship functions
* ManyToManyField.related_name¶

    Same as ForeignKey.related_name.

* ManyToManyField.related_query_name¶

    Same as ForeignKey.related_query_name.

* ManyToManyField.limit_choices_to¶

    Same as ForeignKey.limit_choices_to.
  
* limit_choices_to has no effect when used on a ManyToManyField with a custom intermediate table specified using the through parameter.

* ManyToManyField.symmetrical¶

*    Only used in the definition of ManyToManyFields on self. Consider the following model:
