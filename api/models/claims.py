from db import db

class Claim(db.Model):
    __tablename__ = 'claims'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100))

    def __init__(self, description):
        self.description = description,


    def json(self):
        return {
            "id": self.id,
            "description": self.description,
        }
    @classmethod
    def find_claim(cls, id):
        claim = cls.query.filter_by(id=id).first()
        if claim:
            return claim
        else:
            return None
        
    @classmethod
    def update_claim(cls, claim_id, data):
        claim = cls.find_claim(claim_id)

        if claim != None:
            if 'description' in data and type(data['description']) == str:
                claim.description = data['description']

            db.session.commit()
            return claim
             
        return None
        
    def save_claim(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_claim(cls, id):
        claim = cls.find_claim(id)
        if claim:
            db.session.delete(claim)
            db.session.commit()
            return True
        return None