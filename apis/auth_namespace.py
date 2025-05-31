from flask_restx import Namespace, Resource, fields

api = Namespace('auth')

@api.route('/register-user')
class UserRegister(Resource):
    @api.doc('register')
    def post(self):
        '''Register a new user'''
        
        return {}
    

@api.route('/login')
class UserAuth(Resource):
    @api.doc('authenticate_user')
    def post(self):
        '''Authenticate a user and return a token or session'''
        
        return {}
    
    