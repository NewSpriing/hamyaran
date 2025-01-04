from django.db import migrations, models
from django.db import connection

def convert_time_to_timestamp(apps, schema_editor):
    # Access the cursor for custom SQL
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE account_prescription
            SET "start_date" = current_date + "start_date";  -- Add the current date to the time field
        """)

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_prescription_start_date'),
    ]

    operations = [
        # Run custom SQL to convert time to timestamp by adding the current date
        migrations.RunPython(convert_time_to_timestamp),
        
        # Alter the field to DateTimeField, which combines date and time
        migrations.AlterField(
            model_name='prescription',
            name='start_date',
            field=models.DateTimeField(),  # Change to DateTimeField to include both date and time
        ),
    ]
