#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):

    def post(self):
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User(
            username=username
            )
        user.password_hash = password

        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        
        return UserSchema().dump(user), 201

class Login(Resource):

    def post(self):

        user = User.query.filter(User.username == request.get_json()['username']).first()
        if user:
            session['user_id'] = user.id
            return UserSchema().dump(user), 200
        else:
            return 401

class CheckSession(Resource):

    def get(self):

        user = User.query.filter(User.id == session.get('user_id')).first() # User.id means the id column of the "User" table within the User class. session.get('user_id') retrieves the user's logged in session id number and assigns it to the User.id

        if user:
            return UserSchema().dump(user), 200
        else:
            return {}, 204

class Logout(Resource):

    def delete(self):
        session['user_id'] = None
        return {}


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear', endpoint='clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
