from core.extensions import ma
from models import Plan
from marshmallow.fields import String, Integer
from marshmallow import ValidationError, validates_schema, validate

class PlanSchema(ma.Schema):
    class Meta:
        model = Plan

    name = ma.Str()
    price = ma.Str()
    created_at = ma.DateTime()

class PlanCreateSchema(ma.Schema):
    class Meta:
        model = Plan

    name = String(required=True, validate=[validate.Length(min=3)])
    price = Integer(required=True)

    @validates_schema
    def validate_name(self, data, **kwargs):
        name = data.get("name")
        print("validating name ...")
        if Plan.query.filter_by(name=name).count():
            raise ValidationError(f"Plan {name} already exists.")


