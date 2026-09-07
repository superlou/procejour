from tortoise import migrations
from tortoise.migrations import operations as ops
from orjson import loads
from procejour.models import StepMarkPassFail
from tortoise.fields.base import OnDelete
from tortoise.fields.data import JSON_DUMPS
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0004_add_procedure_to_datasheet')]

    initial = False

    operations = [
        ops.CreateModel(
            name='StepMark',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('step_id', fields.TextField(unique=False)),
                ('datasheet', fields.ForeignKeyField('models.Datasheet', source_field='datasheet_id', db_constraint=True, to_field='id', related_name='step_marks', on_delete=OnDelete.CASCADE)),
                ('observation', fields.JSONField(db_default=None, encoder=JSON_DUMPS, decoder=loads)),
                ('pass_fail', fields.CharEnumField(description='UNSET: un\nPASS: p\nFAIL: f\nDONE: d', db_default='un', enum_type=StepMarkPassFail, max_length=2)),
                ('done', fields.BooleanField()),
                ('timestamp', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('comment', fields.TextField(unique=False)),
            ],
            options={'table': 'stepmark', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
