from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import Avg, Max, Min


class Product(models.Model):
	item = models.CharField(max_length = 50)
	image = models.ImageField(upload_to='media/', height_field=None, width_field=None, max_length=100, null=True, blank=True)
	sound = models.FileField(upload_to='sound/', max_length=100, null=True, blank=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=3)
	discount_price = models.DecimalField(max_digits=10, decimal_places=3)
	manufacturer = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.item

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	area = models.CharField(max_length=255)
	street = models.CharField(max_length=255)
	house = models.CharField(max_length=255)
	block = models.IntegerField(default=1)
	shipping_address = models.TextField(null = True, blank = True)

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	
	def __str__(self):
		return "%s Cart"%self.user

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=3)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

class Order(models.Model):
	ORDER_STATUS = (
	('placed', 'Placed'),
	('paid', 'Paid'),
	('shipped', 'Shipped'),
	('delivered', 'Delivered'))

	status = models.CharField(max_length=120, choices=ORDER_STATUS, default='created')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	area = models.CharField(max_length=255)
	street = models.CharField(max_length=255)
	house = models.CharField(max_length=255)
	block = models.IntegerField()
	order_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	order_date = models.DateTimeField(auto_now_add=True)
	billing_address = models.TextField(null = True, blank = True)



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

	@property
	def calculate_average(self):
		Review.objects.aggregate(Avg('average_rating'))
		return self._calculate_average
	

@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(pre_save, sender = Order)
def get_billing_address(instance, *args, **kwargs):
	instance.billing_address = "Area: %s, Block: %s, Street: %s, House: %s"%(instance.area, instance.block, instance.street, instance.house)

@receiver(pre_save, sender = Profile)
def get_shipping_address(instance, *args, **kwargs):
	instance.shipping_address = "Area: %s, Block: %s, Street: %s, House: %s"%(instance.area, instance.block, instance.street, instance.house)





