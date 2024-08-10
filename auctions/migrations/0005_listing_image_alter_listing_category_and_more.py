# Generated by Django 5.0.1 on 2024-02-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_category_alter_listing_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('ARTS', 'Arts'), ('CHLD', 'Child'), ('BTY', 'Beauty'), ('ELECT', 'Electronics'), ('FSHN', 'Fashion'), ('G&DIY', 'Garden & DYI'), ('AUTO', 'Motorization'), ('REST', 'Real Estates'), ('ENTER', 'Entertainment')], max_length=5),
        ),
        migrations.AlterField(
            model_name='listing',
            name='condition',
            field=models.CharField(choices=[('LN', 'Like New'), ('UG', 'Used - Good'), ('DMG', 'Damaged'), ('N', 'New'), ('UF', 'Used - Fair'), ('UP', 'Used - Poor')], max_length=3),
        ),
    ]
