from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String
from model.pessoa import Pessoa
from model.endereco import endereco_fields

administrador_fields = {

    'id_administrador': fields.Integer(attribute='id_administrador'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'senha': fields.String(attribute='senha'),
    'dt_nasc': fields.String(attribute='dt_nasc'),
    'telefone': fields.String(attribute='telefone'),
    'cpf': fields.String(attribute='cpf'),
    'endereco': fields.Nested(endereco_fields),
    'tipo_pessoa': fields.String(attribute='tipo_pessoa')
    
}

class Administrador(Pessoa, db.Model):

    __tablename__ = "tb_administrador"
    __mapper_args__ = {'polymorphic_identity': 'admin' }
    
    id_administrador = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))
    tipo_pessoa = db.Column('tipo_pessoa', String(50), default='admin')
    
    def __init__(self, nome, email, senha, dt_nasc, cpf, telefone, endereco, foto=None):
        super().__init__(foto, nome, email, senha, dt_nasc, cpf, telefone, endereco)
    def __repr__(self):
        return f'Administrador(E-mail={self.email}, Senha={self.senha}, Nome={self.nome}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereço={self.endereco})'
