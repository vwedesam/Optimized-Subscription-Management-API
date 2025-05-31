from datetime import datetime, timedelta
from flask import request
from sqlalchemy import text
from flask_restx import Namespace, Resource
from core.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.schema.subscription_schema import SubscriptionSchema, SubscriptionCreateSchema
from marshmallow import ValidationError
from core.error_handler import validation_error
from models import Subscription, Plan

api = Namespace('subscriptions')

@api.route('')
class SubscriptionResource(Resource):
    @api.doc('list-subscriptions')
    @jwt_required()
    def get(self):
        '''Retrieve a list of all subscriptions'''
        user_id = get_jwt_identity()

         # Pagination result (fallback to page 1, 10 items per page)
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        offset = (page - 1) * per_page

        sql = text("""
            SELECT *
            FROM subscription
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT :limit 
            OFFSET :offset
        """)

        subscriptions = db.session.execute(sql, {"user_id": user_id, "limit": per_page, "offset": offset}).all()

        schema = SubscriptionSchema(many=True)
        return {
            'data': schema.dump(subscriptions),
            "current_page": page,
            "per_page": per_page
        }
    
    @api.doc('create-subscription')
    @jwt_required()
    def post(self):
        '''Create a new subscription'''

        user_id = get_jwt_identity()
        json = request.json
        try:
            schema = SubscriptionCreateSchema()
            # Validate create subscription request -> throw ValidationError exception if not valid
            schema.load(json)
        except ValidationError as err:
            return validation_error(err)
        
        plan_id = json.get('plan_id')
        
        plan = Plan.query.filter_by(id=plan_id).first()
        # Check if plan exist
        if plan is None:
            return { 'error': f"Plan with id '{plan_id}' does not exists." }, 400
        
        name = plan.name
        price = plan.price
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        created_at = datetime.now()

        subscription = Subscription(plan_id=plan_id, name=name, price=price, is_active=True, user_id=user_id, start_date=start_date, end_date=end_date, created_at=created_at)
        # add to session and commit
        db.session.add(subscription)
        db.session.commit()
        schema = SubscriptionSchema()   
        return schema.dump(subscription)

@api.route('/active')
class subscriptionActive(Resource):
    @api.doc('get-active-subscription')
    @jwt_required()
    def get(self):
        '''Retrieve the currently active subscription for the user'''

        user_id = get_jwt_identity()
        now = datetime.now()

        sql = text("""
            SELECT *
            FROM subscription
            WHERE user_id = :user_id
            AND is_active = TRUE
            AND end_date > :now
            ORDER BY created_at DESC
            LIMIT 1
        """)

        active_subscription = db.session.execute(sql, {"user_id": user_id, "now": now}).first()

        if active_subscription is None:
            return { 'error': f"No active subscription found." }, 404
        
        schema = SubscriptionSchema()
        return schema.dump(active_subscription)

@api.route('/upgrade')
class subscriptionUpgrade(Resource):
    @api.doc('upgrade-subscription')
    @jwt_required()
    def put(self):
        '''Upgrade the current subscription to a higher plan'''

        user_id = get_jwt_identity()
        json = request.json
        try:
            schema = SubscriptionCreateSchema()
            # Validate upgrade subscription request -> throw ValidationError exception if not valid
            schema.load(json)
        except ValidationError as err:
            return validation_error(err)
        
        plan_id = json.get('plan_id')

        plan = Plan.query.filter_by(id=plan_id).first()

        # Check if plan is valid
        if plan is None:
            return { 'error': f"Plan with id '{plan_id}' does not exists." }, 400
        
        active_subscription = Subscription.query.filter_by(user_id=user_id, is_active=True).first()

        if active_subscription is None:
            return { 'error': f"No active subscription found." }, 404

        active_subscription.is_active = False
        active_subscription.end_date = datetime.now()

        # Check if ew plan is the same as current plan
        if int(active_subscription.plan_id) == int(plan_id):
            return { "error": "You're already on this subscription plan. Please select a different plan to upgrade."}, 400

        name = plan.name
        price = plan.price
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        created_at = datetime.now()

        subscription = Subscription(plan_id=plan_id, name=name, price=price, is_active=True, user_id=user_id, start_date=start_date, end_date=end_date, created_at=created_at)
        # add to session and commit
        db.session.add(subscription)
        db.session.commit()
        schema = SubscriptionSchema()
        return schema.dump(subscription)

@api.route('/cancel')
class subscriptionCancel(Resource):
    @api.doc('cancel-subscription')
    @jwt_required()
    def patch(self):
        '''Cancel the current active subscription'''

        user_id = get_jwt_identity()

        current_subscription = Subscription.query.filter_by(user_id=user_id, is_active=True).first()

        if current_subscription:
            current_subscription.is_active = False
            current_subscription.end_date = datetime.now()

        db.session.commit()

        return {
            "success": "ok"
        }
    
    
