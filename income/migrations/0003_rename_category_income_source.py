# Generated by Django 5.0.4 on 2024-05-24 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_alter_income_options_alter_source_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='category',
            new_name='source',
        ),
    ]
