from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
# Create your models here.
class Category(MPTTModel):
	STATUS = (
		('True', 'True'),
		('False', 'False'),
	)
	parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	keywords = models.CharField(max_length=255)
	description = models.TextField(max_length=255)
	status=models.CharField(max_length=10, choices=STATUS)
	slug = models.SlugField(null=False, unique=True)
	create_at=models.DateTimeField(auto_now_add=True)
	update_at=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class MPTTMeta:
		order_insertion_by = ['title']

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'slug': self.slug})

	def __str__(self):                           # __str__ method elaborated later in
		full_path = [self.title]                  # post.  use __unicode__ in place of
		k = self.parent
		while k is not None:
			full_path.append(k.title)
			k = k.parent
		return ' / '.join(full_path[::-1])

# category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Book(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=120)
	description = RichTextUploadingField(default="desc")
	# Sale_Price = models.DecimalField(decimal_places=2,max_digits=100, null=True, blank=True)
	Current_Price = models.DecimalField(decimal_places=2,max_digits=100)
	Listing_Price = models.DecimalField(decimal_places=2,max_digits=100)
	First_Rental_Price = models.DecimalField(decimal_places=2,max_digits=100)
	Second_Rental_Price = models.DecimalField(decimal_places=2,max_digits=100)
	Third_Rental_Price = models.DecimalField(decimal_places=2,max_digits=100)
	Publisher = models.CharField(max_length=100)
	Author = models.CharField(max_length=100)
	ISBN = models.IntegerField(null=True)
	Edition = models.IntegerField(null=True)
	Quality = models.CharField(max_length=120)
	Quantity = models.IntegerField(null=True, default=1)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	image = models.ImageField(upload_to="products/images/",default="")
	
	def __str__(self):
		return self.title

	def get_price(self):
		return self.Listing_Price	

class VariationManager(models.Manager):
	def actions(self):
		return super(VariationManager, self).filter(active=True).filter(cat='action')



VAR_CATEGORIES = (
	('action', 'action'),
	)


class Variation(models.Model):
	product = models.ForeignKey(Book, default=1, on_delete=models.SET_DEFAULT)
	cat = models.CharField(max_length=100,choices=VAR_CATEGORIES, default='action')
	title = models.CharField(max_length=120)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	objects = VariationManager()

	def __str__(self):
		return self.title


class About(models.Model):
	title = models.CharField(max_length=100, default=1)
	firstp = models.CharField(max_length=20000, default=1)
	secondp = models.CharField(max_length=20000, default=1)
	mission = models.CharField(max_length=20000, default=1)
	vision = models.CharField(max_length=20000, default=1)

	def __str__(self):
		return self.title


class rentalsFAQ(models.Model):
	STATUS = (
		('True', 'True'),
		('False', 'False'),
	)
	prioritynumber = models.IntegerField()
	question = models.CharField(max_length=200)
	answer = RichTextUploadingField(default="desc")
	status=models.CharField(max_length=10, choices=STATUS)
	create_at=models.DateTimeField(auto_now_add=True)
	update_at=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question








# class BookImage(models.Model):
# 	book = models.ForeignKey(Book,default=1, on_delete=models.SET_DEFAULT)
# 	image = models.ImageField(upload_to="products/images/")
# 	featured = models.BooleanField(default=False)
# 	thumbnail = models.BooleanField(default=False)
# 	active = models.BooleanField(default=True)
# 	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	
# 	def __str__(self):
# 		return self.book.title