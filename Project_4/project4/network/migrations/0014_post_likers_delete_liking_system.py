# Generated by Django 5.0 on 2024-02-09 07:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_remove_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Liking_System',
        ),
    ]
