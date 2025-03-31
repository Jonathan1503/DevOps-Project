from flask import request, jsonify
from flask_restful import Resource
from models import Blacklist
from database import db
from schemas.blacklist_schema import blacklist_schema
from flask_jwt_extended import jwt_required
import re
import uuid

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        email = data.get("email")
        app_uuid = data.get("app_uuid")
        blocked_reason = data.get("blocked_reason", "")

        if not email or not app_uuid:
            return {"message": "Email and app_uuid are required"}, 400

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return {"message": "Invalid email format"}, 400

        try:
            uuid_obj = uuid.UUID(app_uuid)
            if str(uuid_obj) != app_uuid:
                return {"message": "Invalid UUID format"}, 400
        except ValueError:
            return {"message": "Invalid UUID format"}, 400
        
        if Blacklist.query.filter_by(email=email, app_uuid=app_uuid).first():
            return {"message": "Email already blacklisted for this app"}, 400

        ip_address = request.remote_addr
        new_entry = Blacklist(email=email, app_uuid=app_uuid, ip_address=ip_address, blocked_reason=blocked_reason)

        db.session.add(new_entry)
        db.session.commit()

        return blacklist_schema.dump(new_entry), 201

    @jwt_required()
    def get(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if entry:
            return {"is_blacklisted": True, "blocked_reason": entry.blocked_reason}, 200
        return {"is_blacklisted": False}, 200
