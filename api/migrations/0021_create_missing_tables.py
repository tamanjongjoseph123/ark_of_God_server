# Create all missing tables to fix pagination issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_merge_20260402_1443'),
    ]

    operations = [
        # Check if Course table exists and create it if missing
        migrations.RunSQL(
            "CREATE TABLE IF NOT EXISTS api_course ("
            "id BIGSERIAL PRIMARY KEY, "
            "name VARCHAR(255) NULL, "
            "description TEXT NULL, "
            "image VARCHAR(500) NULL, "
            "category VARCHAR(32) NULL, "
            "created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), "
            "updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()"
            ")",
            reverse_sql="DROP TABLE IF EXISTS api_course"
        ),
        
        # Check if Module table exists and create it if missing
        migrations.RunSQL(
            "CREATE TABLE IF NOT EXISTS api_module ("
            "id BIGSERIAL PRIMARY KEY, "
            "course_id BIGINT NULL, "
            "name VARCHAR(255) NULL, "
            "description TEXT NULL, "
            "image VARCHAR(500) NULL, "
            "created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()"
            ")",
            reverse_sql="DROP TABLE IF EXISTS api_module"
        ),
        
        # Check if CourseVideo table exists and create it if missing
        migrations.RunSQL(
            "CREATE TABLE IF NOT EXISTS api_coursevideo ("
            "id BIGSERIAL PRIMARY KEY, "
            "module_id BIGINT NULL, "
            "name VARCHAR(255) NULL, "
            "description TEXT NULL, "
            "youtube_url VARCHAR(500) NULL, "
            "key_takeaways TEXT NULL, "
            "assignments TEXT NULL, "
            "created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()"
            ")",
            reverse_sql="DROP TABLE IF EXISTS api_coursevideo"
        ),
    ]
