from django.contrib import admin
from .models import Category, Book, CartItem, Order, OrderItem, Profile, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'author']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price_display']
    
    def get_total_price_display(self, obj):
        if obj.pk:
            return f"{obj.get_total_price():,.0f} đ"
        return "-"
    get_total_price_display.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'full_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin người đặt', {
            'fields': ('user', 'full_name', 'email', 'phone', 'address')
        }),
        ('Thông tin đơn hàng', {
            'fields': ('total_price', 'status', 'created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price', 'get_total_price_display']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'book__title']
    
    def get_total_price_display(self, obj):
        return f"{obj.get_total_price():,.0f} đ"
    get_total_price_display.short_description = 'Thành tiền'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'phone']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']

