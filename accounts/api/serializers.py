from rest_framework import serializers
from accounts.models import User
from django.db import transaction


class User_RegistrationSerializer(serializers.ModelSerializer):
    birth_date = serializers.CharField(
        style={'input_type': 'DateField'}, write_only=True)
    picture =  serializers.ImageField(max_length=None, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username',
                  'first_name', 'last_name', 'is_admin', 'is_customer', 'birth_date',
                  'picture', ]
    def profiling(self , account,data):

        Profile = UserProfile.objects.create(
            user=account,
            birth_date= data['birth_date'],
            picture= data['picture'],
        )
        Profile.save()
    @transaction.atomic
    def update(self , instance,validated_data):
        instance.email=validated_data['email']
        instance.username=validated_data['username']
        instance.first_name=validated_data['first_name']
        instance.last_name=validated_data['last_name']
        instance.is_admin=validated_data['is_admin']
        instance.is_customer=validated_data['is_customer']
        instance.set_password(validated_data['password'])
        instance.save()
        self.profiling(instance,data = validated_data)
        return instance
         
    
    @transaction.atomic
    def create(self, validated_data):
        try:
            User.objects.get(email=validated_data['email'])
            return 'error'
        except:
            # print(validated_data)
            password = validated_data['password']
            account = User.objects.create(
                    email=validated_data['email'],
                    username= validated_data['username'],
                    first_name= validated_data['first_name'],
                    last_name= validated_data['last_name'],
                    is_admin= validated_data['is_admin'],
                    is_customer=validated_data['is_customer'],
            )
            account.set_password(password)
            account.save()
            self.profiling(account, data = self.validated_data)
            return account
