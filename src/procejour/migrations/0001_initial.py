from tortoise import migrations
from tortoise.migrations import operations as ops
from orjson import loads
from tortoise.fields.data import JSON_DUMPS
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Procedure',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('title', fields.TextField(unique=False)),
                ('ref_doc', fields.TextField(unique=False)),
                ('ref_rev', fields.TextField(unique=False)),
                ('steps', fields.JSONField(encoder=JSON_DUMPS, decoder=loads)),
            ],
            options={'table': 'procedure', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
