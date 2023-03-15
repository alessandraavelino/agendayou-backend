from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String
from model.pessoa import Pessoa
from model.endereco import endereco_fields
parceiro_fields = {

    'id_parceiro': fields.Integer(attribute='id_parceiro'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'senha': fields.String(attribute='senha'),
    'dt_nasc': fields.String(attribute='dt_nasc'),
    'telefone': fields.String(attribute='telefone'),
    'cpf': fields.String(attribute='cpf'),
    'categoria': fields.String(attribute='categoria'),
    'nome_fantasia': fields.String(attribute='nome_fantasia'),
    'endereco': fields.Nested(endereco_fields),
    
}

class Parceiro(Pessoa, db.Model):

    __tablename__ = "tb_parceiro"
    __mapper_args__ = {'polymorphic_identity': 'parceiro' }
    
    id_parceiro = db.Column(db.Integer, primary_key=True)
    nome_fantasia = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    status_aprovacao = db.Column(db.String(10), nullable=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, nome, email, senha, dt_nasc, cpf, telefone, endereco, nome_fantasia, categoria):
        super().__init__(nome, email, senha, dt_nasc, cpf, telefone, endereco)
        self.email = email
        self.senha = senha
        self.nome_fantasia = nome_fantasia
        self.categoria = categoria

    def __repr__(self):
        return f'Parceiro(E-mail={self.email}, Senha={self.senha}, Nome={self.nome}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereço={self.endereco}, Nome Fantasia={self.nome_fantasia}, Categoria={self.categoria})'
