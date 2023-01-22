from django.contrib import admin

from budget.models import Category, UserStatus, Expense


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'amount',
        'get_users'
    ]

    def get_users(self, obj: Expense):
        return [user for user in obj.users.all()]

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    pass