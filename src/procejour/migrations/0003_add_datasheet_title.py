from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0002_add_procedure_rev_to_datasheet')]

    initial = False

    operations = [
        ops.AddField(
            model_name='ProcedureRev',
            name='datasheet_title',
            field=fields.TextField(db_default='', unique=False),
        ),
    ]
