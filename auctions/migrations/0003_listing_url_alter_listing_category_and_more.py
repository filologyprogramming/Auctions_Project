# Generated by Django 5.0.1 on 2024-02-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='url',
            field=models.URLField(default='https://images.google.com'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FSHN', 'Fashion'), ('REST', 'Real Estates'), ('CHLD', 'Child'), ('ENTER', 'Entertainment'), ('BTY', 'Beauty'), ('AUTO', 'Motorization'), ('ELECT', 'Electronics'), ('ARTS', 'Arts'), ('G&DIY', 'Garden & DYI')], max_length=5),
        ),
        migrations.AlterField(
            model_name='listing',
            name='condition',
            field=models.CharField(choices=[('UP', 'Used - Poor'), ('N', 'New'), ('UG', 'Used - Good'), ('DMG', 'Damaged'), ('LN', 'Like New'), ('UF', 'Used - Fair')], max_length=3),
        ),
    ]
