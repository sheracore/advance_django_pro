from django.contrib.auth import get_user_model, authenticate
# ugettext_lazy is used for show output in screen in for language and currect format
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers 


class UserSerializer(serializers.ModelSerializer):
    """ serializer for the user object"""
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        #extra_kwargs used to add some filted on our fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    #Thie is all from the Django rest framework doc's
    def create(self, validated_date):
        """ create a new user with encrypted password and retuen it"""
        return get_user_model().objects.create_user(**validated_date)
    
    # Purpose of this overwriting this function is that inserted password using set_password 
    def update(self, instance, validated_date):
        """Update a user, setting the password correctly and return it"""
        # pop is like get but needs default always(e.g None)
        password = validated_date.pop('password', None)
        user = super().update(instance, validated_date)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
        )

    def validate(self, attrs):
        """Validte and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
            )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs