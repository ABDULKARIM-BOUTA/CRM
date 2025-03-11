# Generated by Django 5.1.6 on 2025-03-11 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_agent_user_is_organizor'),
        ('categories', '0002_remove_category_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.organization'),
        ),
    ]
