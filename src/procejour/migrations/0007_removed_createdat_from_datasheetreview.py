from tortoise import migrations
from tortoise.migrations import operations as ops

class Migration(migrations.Migration):
    dependencies = [('models', '0006_added_datasheetreview')]

    initial = False

    operations = [
        ops.RemoveField(model_name='DatasheetReview', name='created_at'),
    ]
