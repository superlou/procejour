from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_combine_migrations')]

    initial = False

    operations = [
        ops.AddField(
            model_name='Datasheet',
            name='procedure_rev',
            field=fields.ForeignKeyField('models.ProcedureRev', source_field='procedure_rev_id', db_constraint=True, to_field='id', related_name='datasheets', on_delete=OnDelete.CASCADE),
        ),
    ]
