# Create missing Devotion table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_add_courseapplication'),
    ]

    operations = [
        # Create Devotion table
        migrations.CreateModel(
            name='Devotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('content_type', models.CharField(max_length=10, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('text_content', models.TextField(null=True, blank=True)),
                ('youtube_url', models.URLField(null=True, blank=True)),
                ('devotion_date', models.DateField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
