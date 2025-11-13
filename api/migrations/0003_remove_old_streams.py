from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_alter_upcomingevent_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='stream_type',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='youtube_url',
        ),
    ]
