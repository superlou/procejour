from tortoise import migrations
from tortoise.migrations import operations as ops
from procejour.models import ReviewResult
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0005_add_qa_role_to_user')]

    initial = False

    operations = [
        ops.CreateModel(
            name='DatasheetReview',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('datasheet', fields.ForeignKeyField('models.Datasheet', source_field='datasheet_id', db_constraint=True, to_field='id', related_name='reviews', on_delete=OnDelete.CASCADE)),
                ('reviewer', fields.ForeignKeyField('models.User', source_field='reviewer_id', db_constraint=True, to_field='id', related_name='reviews', on_delete=OnDelete.CASCADE)),
                ('created_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('completed_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('result', fields.CharEnumField(description='INCOMPLETE: i\nPASS: p\nFAIL: f', db_default='i', enum_type=ReviewResult, max_length=2)),
                ('comments', fields.TextField(unique=False)),
            ],
            options={'table': 'datasheetreview', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
