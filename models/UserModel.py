from app import db
from passlib.hash import sha256_crypt

class UserModel(db.Model):
  __tablename__ = 'user'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String)
  email = db.Column(db.String)
  password = db.Column(db.String, nullable=False)
  
  def hash_password(password):
      return sha256_crypt.encrypt(password)
    
  def check_password(password, hashStr):
    return sha256_crypt.verify(password, hashStr)