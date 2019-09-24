from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import Avg, Max, Min
from datetime import date


class Product(models.Model):
	item = models.CharField(max_length = 50)
	image = models.ImageField(upload_to='media/', height_field=None, width_field=None, max_length=100, null=True, blank=True)
	sound = models.FileField(upload_to='sound/', max_length=100, null=True, blank=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=3)
	discount_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
	manufacturer = models.CharField(max_length=255, null=True)
	date_added = models.DateTimeField(auto_now_add = True, null=True, blank=True)

	def __str__(self):
		return self.item

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

class Cart(models.Model):
	ORDER_STATUS = [('cart', 'cart'),
		('placed', 'Placed'),
		('review', 'review'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered')]
	subtotal = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	status = models.CharField(max_length=120, choices=ORDER_STATUS, default='cart')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order_date = models.DateTimeField(auto_now_add=True)
	billing_address = models.TextField(null = True, blank = True)
	date_added = models.DateTimeField(auto_now_add = True, null=True, blank=True)

class Payment(models.Model):
	PAYMENT_CARD = [
	('Knet', 'Knet'),
	('Visa', "Visa"),
	('MC', 'MC')]

	method = models.CharField(max_length=120, choices=PAYMENT_CARD)

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
	quantity = models.IntegerField()
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')

class Address(models.Model):
	CHOICES = (
		('billing', 'billing'),
		('shipping', 'shipping')
		)
	area = models.CharField(max_length=255)
	street = models.CharField(max_length=255)
	house = models.CharField(max_length=255)
	block = models.IntegerField()
	complete_Address = models.TextField()
	address_type = models.CharField(max_length=120, choices=CHOICES, default='created')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_user')
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='address_cart')

class Review(models.Model):
	RATING_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5')
		)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	rating = models.IntegerField(choices=RATING_CHOICES)
	comments = models.TextField()

@receiver(post_save, sender=CartItem)
def add_price(instance, *args, **kwargs):
	total = 0
	for i in instance.cart.cartitems.all():
		total += i.product.price*i.quantity
	instance.cart.subtotal = total
	instance.cart.save()

@receiver(pre_delete, sender=CartItem)
def deduct_price(instance, *args, **kwargs):
		cart = instance.cart
		cart.subtotal -= instance.product.price*instance.quantity
		cart.save()
		
@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(pre_save, sender = Address)
def get_billing_address(instance, *args, **kwargs):
	instance.complete_address = "Area: %s, Block: %s, Street: %s, House: %s"%(instance.area, instance.block, instance.street, instance.house)







