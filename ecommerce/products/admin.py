from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Book, Variation, Category, About, rentalsFAQ
# Register your models here.


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Book,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Book,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'








class BookAdmin(admin.ModelAdmin):
	search_fields = ['title','description','ISBN']
	list_display = ['title','Current_Price','Listing_Price','First_Rental_Price',
					'Second_Rental_Price','Third_Rental_Price','active']
	list_editable = ['Current_Price','Listing_Price','First_Rental_Price',
					'Second_Rental_Price','Third_Rental_Price','active']
	list_filter = ['Current_Price','active']
	readonly_fields = ['updated','timestamp']
	class Meta:
		model = Book


class rentalsFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','prioritynumber','status']
    list_filter = ['status']



admin.site.register(Book, BookAdmin)
admin.site.register(Variation)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(About)
admin.site.register(rentalsFAQ,rentalsFAQAdmin)