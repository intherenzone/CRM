# Generated by Django 2.0.2 on 2018-03-23 19:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('industry', models.CharField(blank=True, choices=[('ADVERTISING', 'ADVERTISING'), ('AGRICULTURE', 'AGRICULTURE'), ('APPAREL & ACCESSORIES', 'APPAREL & ACCESSORIES'), ('AUTOMOTIVE', 'AUTOMOTIVE'), ('BANKING', 'BANKING'), ('BIOTECHNOLOGY', 'BIOTECHNOLOGY'), ('BUILDING MATERIALS & EQUIPMENT', 'BUILDING MATERIALS & EQUIPMENT'), ('CHEMICAL', 'CHEMICAL'), ('COMPUTER', 'COMPUTER'), ('EDUCATION', 'EDUCATION'), ('ELECTRONICS', 'ELECTRONICS'), ('ENERGY', 'ENERGY'), ('ENTERTAINMENT & LEISURE', 'ENTERTAINMENT & LEISURE'), ('FINANCE', 'FINANCE'), ('FOOD & BEVERAGE', 'FOOD & BEVERAGE'), ('GROCERY', 'GROCERY'), ('HEALTHCARE', 'HEALTHCARE'), ('INSURANCE', 'INSURANCE'), ('LEGAL', 'LEGAL'), ('MANUFACTURING', 'MANUFACTURING'), ('PUBLISHING', 'PUBLISHING'), ('REAL ESTATE', 'REAL ESTATE'), ('SERVICE', 'SERVICE'), ('SOFTWARE', 'SOFTWARE'), ('SPORTS', 'SPORTS'), ('TECHNOLOGY', 'TECHNOLOGY'), ('TELECOMMUNICATIONS', 'TELECOMMUNICATIONS'), ('TELEVISION', 'TELEVISION'), ('TRANSPORTATION', 'TRANSPORTATION'), ('VENTURE CAPITAL', 'VENTURE CAPITAL')], max_length=255, null=True, verbose_name='Industry Type')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('is_active', models.BooleanField(default=False)),
                ('assigned_to', models.ManyToManyField(related_name='account_assigned_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
