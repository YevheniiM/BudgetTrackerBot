# Generated by Django 3.2.9 on 2023-01-26 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230126_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='spreadsheet_id',
            new_name='working_sheet_key',
        ),
    ]
