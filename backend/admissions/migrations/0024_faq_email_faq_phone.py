# Generated by Django 5.0.4 on 2024-05-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0023_alter_question_options_remove_question_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
