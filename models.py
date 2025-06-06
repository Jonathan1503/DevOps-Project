from database import db
import datetime

class Blacklist(db.Model):
    __tablename__ = 'blacklists'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('email', 'app_uuid', name='uniq_email_app'),
    )

    def __init__(self, email, app_uuid, ip_address, blocked_reason=None):
        self.email = email
        self.app_uuid = app_uuid
        self.ip_address = ip_address
        self.blocked_reason = blocked_reason
