from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_old_streams'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='is_live',
            field=models.BooleanField(default=False, help_text='Check this if this stream is currently live'),
        ),
        migrations.AddField(
            model_name='stream',
            name='scheduled_time',
            field=models.DateTimeField(blank=True, help_text='Scheduled start time (optional)', null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='stream_url',
            field=models.URLField(help_text='URL of the live stream (YouTube, Facebook, etc.)', validators=[django.core.validators.URLValidator()]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stream',
            name='thumbnail_url',
            field=models.URLField(blank=True, help_text='Optional thumbnail image URL for the stream', null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='description',
            field=models.TextField(blank=True, help_text='Optional description', null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='title',
            field=models.CharField(help_text='Title of the live stream', max_length=255),
        ),
    ]
