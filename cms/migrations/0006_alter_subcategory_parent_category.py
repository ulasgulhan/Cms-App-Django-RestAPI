# Generated by Django 4.2.9 on 2024-01-10 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_alter_pages_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='parent_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='cms.category'),
        ),
    ]
