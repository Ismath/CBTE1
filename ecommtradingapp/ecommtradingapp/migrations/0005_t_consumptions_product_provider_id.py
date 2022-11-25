# Generated by Django 4.1.3 on 2022-11-24 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommtradingapp', '0004_alter_t_product_provider_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_consumptions',
            name='product_provider_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_provider1', to='ecommtradingapp.t_product_provider'),
            preserve_default=False,
        ),
    ]
