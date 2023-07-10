from db import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100))


    def __init__(self, description):
        self.description = description

    def json(self):
        return {
            'id': self.id,
            'description': self.description
        }

    @classmethod
    def find_role(cls, id):
        role = cls.query.filter_by(id=id).first()
        if role:
            return role
        else:
            return None
        
    def save_role(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_role(cls, role_id, data):
        role = cls.find_role(role_id)

        if role != None:
            if 'description' in data and type(data['description']) == str:
                role.description = data['description']

            db.session.commit()
            return role
             
        return None
        

    @classmethod
    def delete_role(cls, id):
        role = cls.find_role(id)
        if role:
            db.session.delete(role)
            db.session.commit()
            return True
        return None
