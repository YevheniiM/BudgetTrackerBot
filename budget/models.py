from enum import Enum

from django.db import models

from users.models import User
from utils.models import CreateUpdateTracker


class Category(CreateUpdateTracker):
    users = models.ManyToManyField(User, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Expense(CreateUpdateTracker):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.category.name, self.amount)


class UserStatusEnum(Enum):
    DEFAULT = "default"
    CHOOSING_CATEGORY = "choosing_category"
    ENTERING_EXPENSE = "entering_expense"
    ENTERING_EXPENSE_MORE_THAN_ONE = "entering_expense_more_than_one"
    EXPENSE_ENTERED = "expense_entered"
    ENTERING_EMAIL = "entering_email"


class UserStatus(CreateUpdateTracker):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=56,
                              choices=[(tag.value, tag.name) for tag in UserStatusEnum],
                              default=UserStatusEnum.DEFAULT)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.user_id, self.status)
