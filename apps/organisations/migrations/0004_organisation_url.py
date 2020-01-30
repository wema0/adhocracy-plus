# Generated by Django 2.2.9 on 2020-01-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_organisations', '0003_collapsible_element'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='url',
            field=models.URLField(blank=True, help_text='Please enter a full url which starts with https:// or http://', verbose_name='Organisation website'),
        ),
    ]