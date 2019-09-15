from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
		refresh = RefreshToken.for_user(user)

		return {
			'refresh': str(refresh),
			'access': str(refresh.access_token),
		}

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(read_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'token']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		validated_data["token"] = get_token(new_user)
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

