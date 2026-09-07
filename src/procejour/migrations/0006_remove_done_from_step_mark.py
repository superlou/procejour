from tortoise import migrations
from tortoise.migrations import operations as ops

class Migration(migrations.Migration):
    dependencies = [('models', '0005_add_step_mark')]

    initial = False

    operations = [
        ops.RemoveField(model_name='StepMark', name='done'),
    ]
