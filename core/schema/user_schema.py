from core.extensions import ma
from models import User
from marshmallow.fields import String
from marshmallow import ValidationError, validates_schema, validate

class UserSchema(ma.Schema):
    class Meta:
        model = User

    email = ma.Str()
    first_name = ma.Str()
    last_name = ma.Str()
    created_at = ma.DateTime()

class UserRegisterSchema(ma.Schema):
    class Meta:
        model = User

    email = String(required=True, validate=[validate.Email()])
    password = String(required=True, validate=[validate.Length(min=6)])
    first_name = String(required=True, validate=[validate.Length(min=3)])
    last_name = String(required=True, validate=[validate.Length(min=3)])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")
        print("validating email ...")
        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")


class UserLoginSchema(ma.Schema):
    class Meta:
        model = User

    email = String(required=True)
    password = String(required=True)

