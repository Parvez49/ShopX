from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from autoslug import AutoSlugField

from versatileimagefield.fields import VersatileImageField

from common.base_model import BaseModelWithUID


class Hero(BaseModelWithUID):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    thumbnail = VersatileImageField(upload_to="hero_images/", null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-title"]


class Category(BaseModelWithUID):
    title = models.CharField(max_length=100)
    icon = VersatileImageField(upload_to="category_icons/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Categories")


class Product(BaseModelWithUID):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = VersatileImageField(upload_to="product_images/", null=True, blank=True)
    slug = AutoSlugField(populate_from="title", unique=True, db_index=True)
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.PROTECT, 
        related_name="products"
    )
    unit_price = models.DecimalField(
		max_digits=6,
		decimal_places=2,
		validators=[MinValueValidator(1)]
	)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    popular_item = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Products"
