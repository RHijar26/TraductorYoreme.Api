ADMINISTRATOR = 1
TRANSLATOR = 2


from DATABASE.db import db
import re

class Roles(db.Model):

    __tablename__ = 'Roles'

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
        
    def __repr__(self):
        return f"<Roles {self.Name}>"