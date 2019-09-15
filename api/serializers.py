from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data


class ListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['item', 'image', 'price']

class DetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
	no_of_items = serializers.SerializerMethodField()
	class Meta:
		model = Cart
		fields = ['items', 'no_of_items']

	def get_no_of_items(self, obj):
		return obj.items.count()

