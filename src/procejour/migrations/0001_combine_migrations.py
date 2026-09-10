from tortoise import migrations
from tortoise.migrations import operations as ops
from orjson import loads
from procejour.models import StepMarkPassFail
from tortoise.fields.base import OnDelete
from tortoise.fields.data import JSON_DUMPS
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Datasheet',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={'table': 'datasheet', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Procedure',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'procedure', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='ProcedureRev',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('procedure', fields.ForeignKeyField('models.Procedure', source_field='procedure_id', db_constraint=True, to_field='id', related_name='revs', on_delete=OnDelete.CASCADE)),
                ('created_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('saved_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('title', fields.TextField(db_default='', unique=False)),
                ('ref_doc', fields.TextField(db_default='', unique=False)),
                ('ref_rev', fields.TextField(db_default='', unique=False)),
                ('steps', fields.JSONField(db_default=[], encoder=JSON_DUMPS, decoder=loads)),
            ],
            options={'table': 'procedurerev', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='StepMark',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('step_id', fields.TextField(unique=False)),
                ('datasheet', fields.ForeignKeyField('models.Datasheet', source_field='datasheet_id', db_constraint=True, to_field='id', related_name='step_marks', on_delete=OnDelete.CASCADE)),
                ('observation', fields.JSONField(db_default=None, encoder=JSON_DUMPS, decoder=loads)),
                ('pass_fail', fields.CharEnumField(description='UNSET: un\nPASS: p\nFAIL: f\nDONE: d', db_default='un', enum_type=StepMarkPassFail, max_length=2)),
                ('timestamp', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('comment', fields.TextField(unique=False)),
            ],
            options={'table': 'stepmark', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='User',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('email', fields.CharField(unique=True, max_length=255)),
                ('name', fields.CharField(default='', max_length=255)),
                ('code', fields.CharField(default='', max_length=255)),
                ('password_hash', fields.CharField(max_length=255)),
                ('admin', fields.BooleanField(default=False)),
                ('api_access', fields.BooleanField(db_default=False)),
            ],
            options={'table': 'user', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='APIKey',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='id', related_name='api_keys', on_delete=OnDelete.CASCADE)),
                ('key', fields.CharField(max_length=255)),
            ],
            options={'table': 'apikey', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
