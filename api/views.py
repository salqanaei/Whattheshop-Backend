from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import AddressSerializer, ReviewSerializer, ProfileSerializer, UserCreateSerializer, ListSerializer, DetailSerializer, CartSerializer, CartItemSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsCreator

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer

class ListAPIView(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'
	permission_classes = [AllowAny]

class CartAPIView(ModelViewSet):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cart_id'
	permission_classes = [AllowAny]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_queryset(self):
		user = self.request.user
		queryset = self.queryset.filter(user=user, status = 'cart')
		return queryset


class CartItemView(ModelViewSet):
	queryset = CartItem.objects.all()
	serializer_class = CartItemSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cartitem_id'
	permission_classes = [AllowAny]
	def create(self, request, *args, **kwargs):
		cart, created = Cart.objects.get_or_create(status='cart', user = request.user)
		cart_item = cart.cartitems.filter(product_id=request.data['product'])
		if not cart_item:
			data = {"product" : request.data['product'], "quantity":request.data['quantity'], "cart": cart.id}
			serializer = self.get_serializer(data=data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)	
		else: 
			cart_item[0].quantity += int(request.data['quantity'])
			cart_item[0].save()
			return Response(request.data, status=status.HTTP_201_CREATED)

	def destroy(self, request, *args, **kwargs):
		cart = Cart.objects.get(status='cart', user = request.user)
		cart_item = cart.cartitems.filter(id=kwargs['cartitem_id'])
		if (cart_item) and (cart_item[0].quantity>1):
			cart_item[0].quantity -= 1
			cart_item[0].save()
			return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
		else: 
			cart_item.delete()
			return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)
	def get_queryset(self):
		user = self.request.user
		cart = Cart.objects.get(status='cart', user = self.request.user)
		queryset = self.queryset.filter(cart = cart.id)
		return queryset

class CartItemDelete(ModelViewSet):
	queryset = CartItem.objects.all()
	serializer_class = CartItemSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cartitem_id'
	permission_classes = [AllowAny]

class CartStatus(APIView):
	queryset = CartItem.objects.all()
	serializer_class = CartSerializer

	def get(self, request, format=None):
		cart = Cart.objects.get(status='cart', user = request.user)
		cart.status = 'placed'
		cart.save()
		return Response({'status': 'success' }, status=status.HTTP_201_CREATED)

class ProfileView(ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'profile_id'
	# permission_classes = [IsAuthenticated, IsAdminUser]

	def get_queryset(self):
		user = self.request.user
		queryset = self.queryset.filter(user=user)
		return queryset

class ReviewView(ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'profile_id'

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class AddressViewSet(ModelViewSet):
	model = Address
	serializer_class = AddressSerializer

	def get_queryset(self,):
		user = self.request.user
		return Address.objects.filter(user=user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

