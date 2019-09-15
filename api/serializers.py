from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
		refresh = RefreshToken.for_user(user)
		return refresh.access_token

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
		fields = ['user', 'product', 'quantity', 'price', 'no_of_items']

	def get_no_of_items(self, obj):
		return obj.product.count()

class CartSerializerUpdate(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["first_name", "last_name"]

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	past_orders = serializers.SerializerMethodField()

	class Meta:
		model = Profile
		fields = ['user', 'area', 'street', 'house', 'block', 'shipping_address', 'past_orders']

	def get_past_orders(self, obj):
		order = Order.objects.filter(user=obj.user, date__lt=date.today())
		return OrderSerializer(orders, many=True).data


