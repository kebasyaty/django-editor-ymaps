# Generated by Django 4.2.5 on 2023-09-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djeym', '0002_status_alter_generalsettings_buttons_text_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='title',
            field=models.CharField(help_text='Examples: Supermarkets of the city of Kharkov | Luxury hotels in Honolulu | Parking of primitive people', max_length=60, unique=True, verbose_name='Title'),
        ),
    ]
