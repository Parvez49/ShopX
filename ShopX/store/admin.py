from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from store.models import Category, Hero, Product


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
	list_display = ["title", "subtitle", "thumbnail"]
	search_fields = ["title"]
	list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	# list_display = ["title", "products_count"]
	list_display = ["title"]
	search_fields = ["title"]

	# @admin.display(ordering="products_count")
	# def products_count(self, category):
	# 	product_list_url  = reverse("admin:store_product_changelist")
	# 	url_queries = urlencode({
	# 		"category_uid": str(category.uid),
	# 	})
	# 	url_with_query_parameters = f"{product_list_url }?{url_queries}"

	# 	return format_html("<a href='{}'>{}</a>", url_with_query_parameters, category.products_count)

	# def get_queryset(self, request):
	# 	return super().get_queryset(request).annotate(products_count=Count("products"))


class InventoryFilter(admin.SimpleListFilter):
	title = "Inventory"
	parameter_name = "inventory"

	less_than_10 = "<10"
	greater_than_50 = ">50"

	def lookups(self, request, model_admin):
		return [
			(self.less_than_10, "Low"),
			(self.greater_than_50, "Greater"),
		]

	def queryset(self, request, queryset):
		if self.value() == self.less_than_10:
			return queryset.filter(inventory__lt=10)

		if self.value() == self.greater_than_50:
			return queryset.filter(inventory__gt=50)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	autocomplete_fields = ["category"]
	actions = ["clear_inventory"]
	list_display = ["title", "unit_price", "inventory_status", "category_title", "slug"]
	list_editable = ["unit_price"]
	list_per_page = 10
	list_select_related = ["category"]
	list_filter = ["category", "updated_at", InventoryFilter]
	search_fields = ["title"]

	@admin.display(ordering="category_title")
	def category_title(self, product):
		return product.category.title

	@admin.display(ordering="inventory")
	def inventory_status(self, product):
		if product.inventory < 10:
			return "Low"
		return "OK"

	@admin.action(description="Clear Inventory")
	def clear_inventory(self, request, queryset):
		updated_count = queryset.update(inventory=0)

		self.message_user(request, message=f"{updated_count} products were successfully updated.")