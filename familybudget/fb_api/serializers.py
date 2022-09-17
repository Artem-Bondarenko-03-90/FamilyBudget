from datetime import time

import kwargs as kwargs
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cat, Week, Sum, Family, Profile


class CatSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Cat
        fields = ('id', 'name', 'type', 'user')

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ('id', 'start_date', 'end_date')

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'name', 'date_create', 'last_modified_date')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'family')

# class UserSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=15)
#     last_login = serializers.DateTimeField(read_only=True, default=None)
#     is_superuser = serializers.BooleanField(default=False)
#     username = serializers.CharField(max_length=30)
#     last_name = serializers.CharField(max_length=30, default=None)
#     email = serializers.EmailField(default=None)
#     is_staff = serializers.BooleanField(default=False)
#     is_active = serializers.BooleanField(default=True)
#     date_joined = serializers.DateTimeField(read_only=True)
#     first_name = serializers.CharField(default=None)
#     family_id = serializers.UUIDField(default=None)
#
#     def create(self, validated_data):
#         user = User(password=self.password, is_superuser=self.is_superuser, username=self.username,
#                     last_name=self.last_name, email=self.email, is_staff=self.is_staff, is_active=self.is_active,
#                     first_name=self.first_name)
#         profile = Profile(user=user.id, family=self.family_id)
#         user.save()
#         profile.save()

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'profile']


    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.save()

        if profile_data != None:
            profile.family = profile_data.get(
                'family',
                profile.family
            )
            profile.save()

        return instance

# class SumSerializer(serializers.Serializer):
#     value = serializers.DecimalField(max_digits=9, decimal_places=2)
#     type = serializers.BooleanField(default=False)
#     date_create = serializers.DateField(read_only=True)
#     last_modified_date = serializers.DateField(read_only=True)
#     cat_id = serializers.UUIDField()
#     week_id = serializers.UUIDField()
#     user_id = serializers.IntegerField()
#     #user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     def create(self, validated_data):
#         return Sum.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.value = validated_data.get("value", instance.value)
#         instance.type = validated_data.get("type", instance.type)
#         instance.last_modified_date = validated_data.get("last_modified_date", instance.last_modified_date)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.week_id = validated_data.get("week_id", instance.week_id)
#         instance.user_id = validated_data.get("user_id", instance.user_id)
#         instance.save()
#         return instance

class SumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sum
        fields = ['id', 'value', 'type', 'date_create', 'last_modified_date', 'cat', 'week', 'user']


    def create(self, validated_data):
        cat = validated_data.pop('cat')
        week = validated_data.pop('week')
        user = validated_data.pop('user')
        sum = Sum.objects.create(**validated_data, cat=cat, week=week, user=user)
        return sum

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.type = validated_data.get('type', instance.type)
        instance.cat = validated_data.get('cat', instance.cat)
        instance.week = validated_data.get('week', instance.week)
        instance.last_modified_date = validated_data.get('last_modified_date', instance.last_modified_date)
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        return instance