from flask_restx import Namespace, Resource, fields

api = Namespace('subscriptions')

@api.route('')
class Subscription(Resource):
    @api.doc('list-subscriptions')
    def get(self):
        '''Retrieve a list of all subscriptions'''
        return []
    
    @api.doc('create-subscription')
    def post(self, id):
        '''Create a new subscription'''
        return {}

@api.route('/active')
class subscription_active(Resource):
    @api.doc('get-active-subscription')
    def get(self, id):
        '''Retrieve the currently active subscription for the user'''
        return {}

@api.route('/upgrade')
class subscription_upgrade(Resource):
    @api.doc('upgrade-subscription')
    def put(self, id):
        '''Upgrade the current subscription to a higher plan'''
        return {}

@api.route('/<sub_id>/cancel')
class subscription_cancel(Resource):
    @api.doc('cancel-subscription')
    def patch(self, sub_id):
        '''Cancel the current active subscription'''

        return { "sub_id": sub_id}
    
