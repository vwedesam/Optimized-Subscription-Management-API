from core.extensions import ma
from models import Subscription
from marshmallow.fields import String
from marshmallow import post_dump

class SubscriptionSchema(ma.Schema):
    class Meta:
        model = Subscription

    id = ma.Str()
    name = ma.Str()
    price = ma.Float()
    start_date = ma.Str()
    end_date = ma.Str()
    is_active = ma.Bool()
    user_id = ma.Str()
    plan_id = ma.Str()
    created_at = ma.Str()

    @post_dump
    def convert_active(self, data, **kwargs):
        # Force conversion
        data['is_active'] = bool(data.get('is_active', 0))
        return data

class SubscriptionCreateSchema(ma.Schema):
    class Meta:
        model = Subscription

    plan_id = String(required=True)

