from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String
from model.pessoa import Pessoa
from model.endereco import endereco_fields

cliente_fields = {

    'id_cliente': fields.Integer(attribute='id_cliente'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'senha': fields.String(attribute='senha'),
    'dt_nasc': fields.String(attribute='dt_nasc'),
    'telefone': fields.String(attribute='telefone'),
    'cpf': fields.String(attribute='cpf'),
    'endereco': fields.Nested(endereco_fields),
    
}

class Cliente(Pessoa, db.Model):

    __tablename__ = "tb_cliente"
    __mapper_args__ = {'polymorphic_identity': 'cliente' }
    
    id_cliente = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, nome, email, senha, dt_nasc, cpf, telefone, endereco):
        super().__init__(nome, email, senha, dt_nasc, cpf, telefone, endereco)
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f'Cliente(E-mail={self.email}, Senha={self.senha}, Nome={self.nome}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereço={self.endereco})'
