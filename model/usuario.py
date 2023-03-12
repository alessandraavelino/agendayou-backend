from helpers.database import db
from flask_restful import fields

from werkzeug.security import generate_password_hash, check_password_hash

usuario_fields = {

    'id_usuario': fields.Integer(attribute='id_usuario'),
    'email': fields.String(attribute='email'),
    'senha': fields.String(attribute='senha')

}

class Usuario(db.Model):

    __tablename__ = "tb_usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(256), nullable=False)

    def __init__(self, email, senha):
        self.email = email
        self.set_senha = senha

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, value):
        return check_password_hash(self.senha, value)
    
    def __repr__(self):
        return f'Usuário(E-mail={self.email}, Senha={self.senha})'
