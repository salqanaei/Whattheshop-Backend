from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import UserCreateSerializer, ListSerializer, DetailSerializer, CartSerializer
from .models import *

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

class CartAPIView(CreateAPIView):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cart_id'

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
