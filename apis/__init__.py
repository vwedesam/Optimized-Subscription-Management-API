from flask_restx import Api

from .auth_namespace import api as auth_namespace
from .plan_namespace import api as plan_namespace
from .subscription_namespace import api as subscription_namespace

api = Api(
    title='Subscription Management API',
    version='1.0',
    description='API for user registration, authentication, and managing subscription plans (Free, Basic, Pro).',
    doc='/api-docs',
    prefix='/api',
    default_mediatype='application/json'  # Set content type
)

# Add routers to api namespace
api.add_namespace(auth_namespace)
api.add_namespace(plan_namespace)
api.add_namespace(subscription_namespace)

