# Generated by Django 5.0.4 on 2024-05-20 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_category_options_alter_category_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='desrcription',
            new_name='description',
        ),
    ]