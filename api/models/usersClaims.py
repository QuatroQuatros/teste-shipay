from db import db

class UserClaim(db.Model):
    __tablename__ = 'user_claims'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), primary_key=True)

    def __init__(self, user_id, claim_id):
        self.user_id = user_id
        self.claim_id = claim_id

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'claim_id': self.claim_id,
        }

    @classmethod
    def find_userClaim(cls, id):
        userClaim = cls.query.filter_by(id=id).first()
        if userClaim:
            return userClaim
        else:
            return None
        
    def save_userClaim(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_userClaim(cls, id, data):
        userClaim = cls.find_userClaim(id)

        if userClaim != None:
            if 'user_id' in data and type(data['user_id']) == int:
                userClaim.user_id = data['user_id']

            if 'claim_id' in data and type(data['claim_id']) == int:
                userClaim.user_id = data['claim_id']

            db.session.commit()
            return userClaim
             
        return None
        

    @classmethod
    def delete_userClaim(cls, id):
        userClaim = cls.find_userClaim(id)
        if userClaim:
            db.session.delete(userClaim)
            db.session.commit()
            return True
        return None