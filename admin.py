from django.contrib import admin
from blog.models import Post, Special, SpecialCondition, Bonuses, BonusShopItem
from cart.models import Cart, CartItem
from buy.models import Buy, BuyItem

admin.site.register(Cart)

admin.site.register(CartItem)

class BuyItemAdmin(admin.ModelAdmin):
    list_display = ('buy', 'user', 'post', 'quantity')  # Отображаем покупку, пользователя, пост и количество
    list_filter = ('buy__created_at', 'buy__user', 'post', 'quantity')  # Фильтры по посту и количеству
    search_fields = ('buy__user__username', 'post__title')  # Поиск по имени пользователя и названию поста
    ordering = ('-buy__created_at',)  # Сортировка по дате создания покупки
    
    # Метод для отображения пользователя, связанного с покупкой
    def user(self, obj):
        return obj.buy.user.username  # Доступ к пользователю через связанную покупку
    user.short_description = 'User'  # Задаем подпись для поля

class BuyItemInline(admin.TabularInline):  # Можно использовать Stackable или Tabular
    model = BuyItem
    extra = 0  # Число пустых форм для добавления новых записей
    fields = ('post', 'quantity')  # Поля, которые должны отображаться в инлайне
    readonly_fields = ('post', 'quantity')

admin.site.register(BuyItem, BuyItemAdmin)

class BuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    
    inlines = [BuyItemInline]

    def user(self, obj):
        return obj.user.username
    user.short_description = 'User'

admin.site.register(Buy, BuyAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображение в списке
    list_display = ('title', 'author', 'display_image', 'cost')
    list_display_links = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'body')
    
    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'body')
        }),
        ('Медиа и цена', {
            'fields': ('image', 'cost'),
            'classes': ('collapse',)
        }),
    )
    
    # Кастомное отображение изображения
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    display_image.short_description = 'Превью'
    
    # Автоматическое заполнение автора
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Только при создании
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    # Оптимизация запросов
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(BonusShopItem)
class BonusShopItemAdmin(admin.ModelAdmin):
    # Отображение в списке
    list_display = ('title', 'author', 'display_image', 'cost')
    list_display_links = ('title', 'author')
    list_filter = ('author',)
    search_field = ('title')
    
    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author')
        }),
        ('Медиа и цена', {
            'fields': ('image', 'cost'),
            'classes': ('collapse',)
        }),
    )
    
    # Кастомное отображение изображения
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    display_image.short_description = 'Превью'
    
    # Автоматическое заполнение автора
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Только при создании
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    # Оптимизация запросов
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(Bonuses)
class BonusesAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_bonus')  # Столбцы в списке
    search_fields = ('user__username',)        # Поиск по имени пользователя
    list_filter = ('bonus_count',)             # Фильтр по количеству бонусов
    raw_id_fields = ('user',)                  # Для удобного выбора пользователя

    def formatted_bonus(self, obj):
        return f"🎁 {obj.bonus_count} бонусов"  # Кастомное отображение
    formatted_bonus.short_description = 'Бонусы'

class SpecialConditionInline(admin.TabularInline):  # или admin.StackedInline
    model = Special.condition.through
    extra = 1

@admin.register(SpecialCondition)
class SpecialConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'promocode', 'discount', 'start_date', 'end_date', 'display_conditions')
    list_filter = ('author', 'start_date', 'end_date')
    search_fields = ('name', 'promocode', 'body')
    filter_horizontal = ('condition',)  
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('name', 'author', 'body')
        }),
        ('Promo Details', {
            'fields': ('promocode', 'condition', 'discount', 'start_date', 'end_date'),
            'classes': ('collapse',)
        }),
    )
    
    def display_conditions(self, obj):
        return ", ".join([cond.name for cond in obj.condition.all()])
    display_conditions.short_description = 'Conditions'

