# Generated by Django 5.1.5 on 2025-04-11 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitelink',
            name='was_created',
            field=models.DateField(auto_created=True),
        ),
    ]
