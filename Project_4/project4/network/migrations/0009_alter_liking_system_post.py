# Generated by Django 5.0 on 2024-02-08 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_liking_system_liked_posts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liking_system',
            name='post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to='network.post'),
        ),
    ]
