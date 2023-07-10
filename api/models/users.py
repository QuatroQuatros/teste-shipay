from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    password = db.Column(db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("Role", backref="users")

    def __init__(self, name, email, password, role_id):
        self.name = name,
        self.email = email,
        self.password = password
        self.role_id = role_id


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # "password": self.password,
            "role_id": self.role_id,
        }
    
    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        else:
            return None
        
    @classmethod
    def update_user(cls, user_id, data):
        user = cls.find_user(user_id)

        if user != None:
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                user.email = data['email']
            if 'role_id' in data:
                user.role_id = data['role_id']

            db.session.commit()
            return user
             
        return None
        
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_user(cls, id):
        user = cls.find_user(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return None


    

