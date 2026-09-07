from enum import Enum, EnumCheck

from tortoise import fields, models
from tortoise.fields import CharEnumField


class Procedure(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.TextField(db_default="")
    ref_doc = fields.TextField(db_default="")
    ref_rev = fields.TextField(db_default="")
    steps = fields.JSONField(db_default=[])

    root_procedure: fields.ForeignKeyNullableRelation["Procedure"] = (
        fields.ForeignKeyField(
            "models.Procedure", related_name="derived_procedures", null=True
        )
    )
    parent_procedure: fields.ForeignKeyNullableRelation["Procedure"] = (
        fields.ForeignKeyField(
            "models.Procedure", related_name="child_procedure", null=True
        )
    )

    # todo Add calculated field identifying if a datasheet exists


class Datasheet(models.Model):
    id = fields.IntField(primary_key=True)
    procedure: fields.ForeignKeyRelation[Procedure] = fields.ForeignKeyField(
        "models.Procedure", related_name="datasheets"
    )


class StepMarkPassFail(Enum):
    UNSET = "un"
    PASS = "p"
    FAIL = "f"
    DONE = "d"


class StepMark(models.Model):
    id = fields.IntField(primary_key=True)
    step_id = fields.TextField()
    datasheet: fields.ForeignKeyRelation[Datasheet] = fields.ForeignKeyField(
        "models.Datasheet", related_name="step_marks"
    )
    observation = fields.JSONField(db_default=None)
    pass_fail = fields.CharEnumField(StepMarkPassFail, db_default="un", max_length=2)
    timestamp = fields.DateTimeField(auto_now=True)
    comment = fields.TextField()
