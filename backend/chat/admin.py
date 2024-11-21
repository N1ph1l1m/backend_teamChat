from django.contrib import admin
from .models import Message, Room, Photos, Documents , ReactionToMessage

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host')  # Список полей, отображаемых в админке
    search_fields = ('name',)  # Поля, по которым можно выполнять поиск
    list_filter = ('host',)  # Фильтры для списка

    # Определите, какие поля показывать на странице изменения модели
    fieldsets = (
        (None, {'fields': ('name', 'host', 'current_users')}),  # Убедитесь, что все поля корректны
    )
    
    # Поля, отображаемые на форме создания/изменения модели
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'host', 'current_users'),
        }),
    )

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id','image')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id','document')

class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id',"id_user", 'emoji')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'text', 'created_at')  # Пример полей, отображаемых в админке
    search_fields = ('text',)  # Поля, по которым можно выполнять поиск
    list_filter = ('room', 'user')  # Фильтры для списка

# Регистрируем модели и их админ-классы
admin.site.register(Room, RoomAdmin)
admin.site.register(Photos,PhotoAdmin)
admin.site.register(Documents,DocumentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ReactionToMessage, ReactionAdmin)

