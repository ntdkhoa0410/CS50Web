# Generated by Django 5.0 on 2024-02-08 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_liking_system_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liking_system',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to='network.post'),
        ),
    ]
