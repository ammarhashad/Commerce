# Generated by Django 3.1.4 on 2021-02-15 10:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210213_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='close',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('how_comment', models.ManyToManyField(blank=True, related_name='comment', to=settings.AUTH_USER_MODEL)),
                ('list_comment', models.ManyToManyField(blank=True, related_name='comment', to='auctions.Listings')),
            ],
        ),
        migrations.CreateModel(
            name='bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField()),
                ('number_of_bid', models.IntegerField()),
                ('Which_bid', models.ManyToManyField(blank=True, related_name='bids', to='auctions.Listings')),
                ('how_bid', models.ManyToManyField(blank=True, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
