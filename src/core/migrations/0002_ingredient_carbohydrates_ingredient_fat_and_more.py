# Generated by Django 4.2.4 on 2023-12-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='carbohydrates',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='fat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='protein',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
