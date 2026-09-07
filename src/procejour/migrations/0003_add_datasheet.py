from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0002_add_defaults')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Datasheet',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
            ],
            options={'table': 'datasheet', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.AddField(
            model_name='Procedure',
            name='parent_procedure',
            field=fields.ForeignKeyField('models.Procedure', source_field='parent_procedure_id', null=True, db_constraint=True, to_field='id', related_name='child_procedure', on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Procedure',
            name='root_procedure',
            field=fields.ForeignKeyField('models.Procedure', source_field='root_procedure_id', null=True, db_constraint=True, to_field='id', related_name='derived_procedures', on_delete=OnDelete.CASCADE),
        ),
    ]
