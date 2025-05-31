from flask_restx import Namespace, Resource, fields

api = Namespace('plans')

@api.route('')
class Plan(Resource):
    @api.doc('list-plans')
    def get(self):
        '''Retrieve a list of all available subscription plans'''
        return []

    @api.doc('create-subscription-plans')
    def post(self):
        '''Create a new subscription plan'''

        return {}

