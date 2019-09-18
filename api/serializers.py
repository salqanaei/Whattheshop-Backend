from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from django.db.models import Avg


def get_token(user):
		refresh = RefreshToken.for_user(user)
		return refresh.access_token

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	access = serializers.CharField(read_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'access']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		validated_data["access"] = get_token(new_user)
		return validated_data


class ListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['item', 'image', 'price', 'description', 'manufacturer', 'date_added']

class DetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = CartItem
		fields = ['product', 'quantity', 'cart']

class CartSerializer(serializers.ModelSerializer):
	cart_items = serializers.SerializerMethodField()
	class Meta: 
		model = Cart
		fields = ['user', 'cart_items', 'subtotal', 'status']
	def get_cart_items(self, obj):
		cartitem = CartItem.objects.all()
		return CartItemSerializer(cartitem, many=True).data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["first_name", "last_name"]

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	past_orders = serializers.SerializerMethodField()

	class Meta:
		model = Profile
		fields = ['user', 'past_orders']

	def get_past_orders(self, obj):
		order = Cart.objects.filter(user=obj.user).exclude(status = 'cart')
		return CartSerializer(order, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ['item', 'rating', 'comments', 'average_rating']

	def get_average_rating(self, obj):
		rating = Review.objects.filter(item = obj.item)

		return rating.aggregate(Avg('rating'))
		 

