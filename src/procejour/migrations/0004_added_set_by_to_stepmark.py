from tortoise import fields, migrations
from tortoise.fields.base import OnDelete
from tortoise.migrations import RunPython
from tortoise.migrations import operations as ops

from procejour.models import StepMark, User


class Migration(migrations.Migration):
    dependencies = [("models", "0003_add_datasheet_title")]

    initial = False

    async def run_forwards(apps, schema_editor):
        user = await User.first()
        await StepMark.all().update(set_by=user)

    operations = [
        ops.AddField(
            model_name="StepMark",
            name="set_by",
            field=fields.ForeignKeyField(
                "models.User",
                source_field="set_by_id",
                null=True,
                db_constraint=True,
                to_field="id",
                related_name="step_marks",
                on_delete=OnDelete.CASCADE,
            ),
        ),
        RunPython(run_forwards),
        ops.AlterField(
            model_name="StepMark",
            name="set_by",
            field=fields.ForeignKeyField(
                "models.User",
                source_field="set_by_id",
                db_constraint=True,
                to_field="id",
                related_name="step_marks",
                on_delete=OnDelete.CASCADE,
            ),
        ),
    ]
