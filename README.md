# advance_django_pro
advance django project with TDD, Travis CI and flake8

#### In this project all admin, models, code handled in core app

### Using mixins
#### One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.
#### The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.
```
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

### ModelSeializer VS serializer
#### The ModelSerializer class is the same as a regular Serializer class, except that:
* It will automatically generate a set of fields for you, based on the model.
* It will automatically generate validators for the serializer, such as unique_together validators.
* It includes simple default implementations of .create() and .update().
#### PUT VS PATCH
* In put your method, request should contain entire fields but in PATHCH you can provide just one changed fied like jast username or just name
