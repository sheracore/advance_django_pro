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
```
from django.db import models

class Person(models.Model):
    friends = models.ManyToManyField("self")
```
#### Some Example
```
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)
```
    Membership has two foreign keys to Person (person and inviter), which makes the relationship ambiguous and Django can’t know which one to use. In this case, you must explicitly specify which foreign keys Django should use using through_fields, as in the example above.

    through_fields accepts a 2-tuple ('field1', 'field2'), where field1 is the name of the foreign key to the model the ManyToManyField is defined on (group in this case), and field2 the name of the foreign key to the target model (person in this case).

    When you have more than one foreign key on an intermediary model to any (or even both) of the models participating in a many-to-many relationship, you must specify through_fields. This also applies to recursive relationships when an intermediary model is used and there are more than two foreign keys to the model, or you want to explicitly specify which two Django should use.

    Recursive relationships using an intermediary model are always defined as non-symmetrical – that is, with symmetrical=False – therefore, there is the concept of a “source” and a “target”. In that case 'field1' will be treated as the “source” of the relationship and 'field2' as the “target”.

ManyToManyField.db_table¶

    The name of the table to create for storing the many-to-many data. If this is not provided, Django will assume a default name based upon the names of: the table for the model defining the relationship and the name of the field itself.

ManyToManyField.db_constraint¶

    Controls whether or not constraints should be created in the database for the foreign keys in the intermediary table. The default is True, and that’s almost certainly what you want; setting this to False can be very bad for data integrity. That said, here are some scenarios where you might want to do this:

        You have legacy data that is not valid.
        You’re sharding your database.

    It is an error to pass both db_constraint and through.

ManyToManyField.swappable¶

    Controls the migration framework’s reaction if this ManyToManyField is pointing at a swappable model. If it is True - the default - then if the ManyToManyField is pointing at a model which matches the current value of settings.AUTH_USER_MODEL (or another swappable model setting) the relationship will be stored in the migration using a reference to the setting, not to the model directly.

    You only want to override this to be False if you are sure your model should always point towards the swapped-in model - for example, if it is a profile model designed specifically for your custom user model.

    If in doubt, leave it to its default of True.

ManyToManyField does not support validators.

null has no effect since there is no way to require a relationship at the database level.


#### An other example for ManyToMany
```
from django.db import models

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']
```

#### So we have:
```
>>> r = Reporter(first_name='John', last_name='Smith', email='john@example.com')
>>> r.save()

>>> r2 = Reporter(first_name='Paul', last_name='Jones', email='paul@example.com')
>>> r2.save()
```

#### Create an Article:
```
>>> from datetime import date
>>> a = Article(id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
>>> a.save()

>>> a.reporter.id
1

>>> a.reporter
<Reporter: John Smith>
```

#### Note that you must save an object before it can be assigned to a foreign key relationship. For example, creating an Article with unsaved Reporter raises ValueError:
```
>>> r3 = Reporter(first_name='John', last_name='Smith', email='john@example.com')
>>> Article.objects.create(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r3)
Traceback (most recent call last):
...
ValueError: save() prohibited to prevent data loss due to unsaved related object 'reporter'.
```
#### Article objects have access to their related Reporter objects:
```

