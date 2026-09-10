from enum import Enum, EnumCheck

from tortoise import fields, models
from tortoise.fields import (
    BooleanField,
    CharEnumField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    ForeignKeyNullableRelation,
    ForeignKeyRelation,
    IntField,
    JSONField,
    ManyToManyRelation,
    TextField,
)


class Procedure(models.Model):
    id = IntField(primary_key=True)
    # Tortoise cannot create a model which only has an auto ID field, so
    # created_at is a dummy value.
    created_at = fields.DatetimeField(auto_now_add=True)

    revs: ManyToManyRelation["ProcedureRev"]

    @property
    async def current_rev(self) -> "ProcedureRev":
        result = await self.revs.order_by("-saved_at").first()
        if result is None:
            raise Exception("Procedure is always expected to have a rev!")
        return result


class ProcedureRev(models.Model):
    id = IntField(primary_key=True)
    procedure: ForeignKeyRelation[Procedure] = ForeignKeyField(
        "models.Procedure", related_name="revs"
    )
    created_at = DateTimeField(auto_now=True)
    saved_at = DateTimeField(auto_now=True)

    title = TextField(db_default="")
    ref_doc = TextField(db_default="")
    ref_rev = TextField(db_default="")
    steps = JSONField(db_default=[])

    datasheets: ManyToManyRelation["Datasheet"]


class Datasheet(models.Model):
    id = IntField(primary_key=True)
    created_at = DateTimeField(auto_now=True)
    procedure_rev: ForeignKeyRelation[ProcedureRev] = ForeignKeyField(
        "models.ProcedureRev", related_name="datasheets"
    )


class StepMarkPassFail(Enum):
    UNSET = "un"
    PASS = "p"
    FAIL = "f"
    DONE = "d"


class StepMark(models.Model):
    id = IntField(primary_key=True)
    step_id = TextField()
    datasheet: ForeignKeyRelation[Datasheet] = ForeignKeyField(
        "models.Datasheet", related_name="step_marks"
    )
    observation = JSONField(db_default=None)
    pass_fail = CharEnumField(StepMarkPassFail, db_default="un", max_length=2)
    timestamp = DateTimeField(auto_now=True)
    comment = TextField()


class User(models.Model):
    id = IntField(pk=True)
    email = CharField(max_length=255, unique=True)
    name = CharField(max_length=255, default="")
    code = CharField(max_length=255, default="")
    password_hash = CharField(max_length=255)
    admin = BooleanField(default=False)
    api_access = BooleanField(db_default=False)


class APIKey(models.Model):
    id = IntField(pk=True)
    user = ForeignKeyField("models.User", related_name="api_keys")
    key = CharField(max_length=255)
