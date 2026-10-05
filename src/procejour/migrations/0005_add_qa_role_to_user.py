from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0004_added_set_by_to_stepmark')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='User',
            name='admin',
            field=fields.BooleanField(db_default=False),
        ),
        ops.AddField(
            model_name='User',
            name='qa',
            field=fields.BooleanField(db_default=False),
        ),
    ]
