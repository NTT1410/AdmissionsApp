# Generated by Django 5.0.4 on 2024-04-25 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0006_alter_banner_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissions',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='banner',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
