# Generated by Django 3.2.9 on 2023-01-22 19:07

import budget.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_auto_20230122_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='status',
            field=models.CharField(choices=[('default', 'DEFAULT'), ('choosing_category', 'CHOOSING_CATEGORY'), ('entering_expense', 'ENTERING_EXPENSE'), ('expense_entered', 'EXPENSE_ENTERED')], default=budget.models.UserStatusEnum['DEFAULT'], max_length=56),
        ),
    ]
