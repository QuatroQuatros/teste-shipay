from db import db

class UserClaim(db.Model):
    __tablename__ = 'user_claims'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), primary_key=True)