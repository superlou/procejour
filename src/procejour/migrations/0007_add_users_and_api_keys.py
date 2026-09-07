from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0006_remove_done_from_step_mark')]

    initial = False

    operations = [
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
