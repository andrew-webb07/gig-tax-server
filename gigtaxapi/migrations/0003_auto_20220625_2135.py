# Generated by Django 3.2.8 on 2022-06-25 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigtaxapi', '0002_auto_20220113_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='category',
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_number',
            field=models.CharField(max_length=100),
        ),
    ]