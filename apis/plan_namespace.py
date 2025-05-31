from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource
from core.schema.plan_schema import PlanSchema, PlanCreateSchema
from marshmallow import ValidationError
from core.error_handler import validation_error
from core.extensions import db
from models import Plan

api = Namespace('plans')

@api.route('')
class plan(Resource):
    @api.doc('list-plans')
    def get(self):
        '''Retrieve a list of all available subscription plans'''

        plans = Plan.query.all()

        planSchema = PlanSchema(many=True)
        return planSchema.dump(plans)  

    @api.doc('create-subscription-plans')
    def post(self):
        '''Create a new subscription plan'''

        json = request.json
        try:
            schema = PlanCreateSchema()
            # Validate create plan request -> throw ValidationError exception if not valid
            valid_plan_request = schema.load(json)
        except ValidationError as err:
            return validation_error(err)

        created_at = datetime.now()
        plan = Plan(**valid_plan_request, created_at=created_at)
        # add to session and commit
        db.session.add(plan)
        db.session.commit()
        # transform plan object
        planSchema = PlanSchema()
        return planSchema.dump(plan)    

