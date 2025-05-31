from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource
from models import User
from marshmallow import ValidationError
from core.schema.user_schema import UserLoginSchema, UserRegisterSchema, UserSchema
from core.error_handler import validation_error
from core.extensions import db
from flask_jwt_extended import create_access_token

api = Namespace('auth')

@api.route('/register-user')
class UserRegister(Resource):
    @api.doc('register')
    def post(self):
        '''Register a new user'''
        json = request.json
        try:
            schema = UserRegisterSchema()
            # Validate register user request -> throw ValidationError exception if not valid
            valid_user_request = schema.load(json)
        except ValidationError as err:
            return validation_error(err)

        created_at = datetime.now()
        user = User(**valid_user_request, created_at=created_at)
        # add to session and commit
        db.session.add(user)
        db.session.commit()
        # transform user object
        userSchema = UserSchema()
        return userSchema.dump(user)
    

@api.route('/login')
class UserAuth(Resource):
    @api.doc('authenticate_user')
    def post(self):
        '''Authenticate a user and return a token or session'''
        json = request.json
        try:
            schema = UserLoginSchema()
            # Validate auth request -> throw ValidationError exception if not valid
            schema.load(json)
        except ValidationError as err:
            return validation_error(err)
        
        email = json.get('email')
        password = json.get('password')
        user = User.query.filter_by(email=email).first()

        if user is None:
            return { 'error': "Password or Email not correct." }, 400

        is_valid = user.check_password(password)

        if is_valid == False:
            return { 'error': "Password or Email not correct." }, 400

        auth_token = create_access_token(str(user.id))

        return {
            "token": auth_token
        }
    
    