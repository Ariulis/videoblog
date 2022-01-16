from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required


from . import auth
from .. import db, logger, docs
from ..models import User
from ..schemas import UserSchema, AuthSchema
from ..base_view import BaseView


class ProfileView(BaseView):
    @jwt_required()
    @marshal_with(UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception('User is not found')
        except Exception as e:
            logger.warning(
                f'user: {user_id} failed to read profile: {e}')
            return {
                'message': str(e)
            }, 400
        return user


@auth.route('/login', methods=['POST'])
@marshal_with(AuthSchema)
@use_kwargs(UserSchema(only=('email', 'password')))
@logger.catch
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.generate_authorization_token()
    except Exception as e:
        logger.warning(
            f'loging with email {kwargs["email"]} failed with errors: {e}')
        return {
            'message': str(e)
        }, 400
    return {
        'access_token': token
    }


@auth.route('/register', methods=['POST'])
@marshal_with(AuthSchema)
@use_kwargs(UserSchema)
@logger.catch
def register(**kwargs):
    try:
        new_user = User(**kwargs)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        logger.warning(
            f'Registration failed with error: {e}')
        return {
            'message': e
        }, 400
    token = new_user.generate_authorization_token()
    return {
        'access_token': token
    }


docs.register(login, blueprint="auth")
docs.register(register, blueprint="auth")

ProfileView.register(auth, docs, '/profile', 'profileview')
