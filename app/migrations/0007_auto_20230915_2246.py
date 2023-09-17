from django.db import migrations
from psqlextra.backend.migrations.operations import PostgresAddRangePartition


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0006_auto_20230915_2245'),
    ]

    operations = [
        PostgresAddRangePartition(
            model_name="postmodel",
            name="post_partitioned_create_from_2022_to_2023",
            from_values='2022-01-01',
            to_values='2023-12-31',
        ),
    ]
