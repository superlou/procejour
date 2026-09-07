from tortoise import migrations
from tortoise.migrations import operations as ops
from orjson import loads
from tortoise.fields.data import JSON_DUMPS
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='Procedure',
            name='ref_doc',
            field=fields.TextField(db_default='', unique=False),
        ),
        ops.AlterField(
            model_name='Procedure',
            name='ref_rev',
            field=fields.TextField(db_default='', unique=False),
        ),
        ops.AlterField(
            model_name='Procedure',
            name='steps',
            field=fields.JSONField(db_default=[], encoder=JSON_DUMPS, decoder=loads),
        ),
        ops.AlterField(
            model_name='Procedure',
            name='title',
            field=fields.TextField(db_default='', unique=False),
        ),
    ]
