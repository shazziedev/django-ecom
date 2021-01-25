from django.contrib import admin

from .models import * 


admin.site.register([moreImgDetails,Category])
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'is_pub', 'current_price', 'timestamp')
    list_filter = ('is_pub', 'timestamp', 'price')
    search_fields = ('name', 'info', 'price')
    actions = ['publish','draft']

    def publish(self, request, queryset):
        queryset.update(is_pub=True)

    def draft(self, request, queryset):
    	queryset.update(is_pub=False)
