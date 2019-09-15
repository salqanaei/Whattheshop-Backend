from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserCreateSerializer, ListSerializer, DetailSerializer, CartSerializer, CartSerializerUpdate
from .models import *
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer

class ListAPIView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ListSerializer

class DetailAPIView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = DetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'

class CartAPIView(ModelViewSet):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cart_id'

	def get_serializer_class(self):
		if self.action == "update":
			return CartSerializerUpdate

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
