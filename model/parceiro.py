from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String
from model.pessoa import Pessoa
parceiro_fields = {

    'id_parceiro': fields.Integer(attribute='id_parceiro'),
    'categoria': fields.String(attribute='categoria'),
    'status_aprovacao': fields.String(attribute='status_aprovacao'),
}

class Parceiro(Pessoa, db.Model):

    __tablename__ = "tb_parceiro"
    __mapper_args__ = {'polymorphic_identity': 'parceiro' }
    
    id_parceiro = db.Column(db.Integer, primary_key=True)
    nome_fantasia = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    status_aprovacao = db.Column(db.String(10), nullable=False)

    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, nome, dt_nasc, cpf, telefone, endereco, nome_fantasia, categoria, status_aprovacao):
        super().__init__(nome, dt_nasc, cpf, telefone, endereco)
        self.nome_fantasia = nome_fantasia
        self.categoria = categoria
        self.status_aprovacao = status_aprovacao

    def __repr__(self):
        return f'Parceiro(Nome={self.nome}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereço={self.endereco}, Nome Fantasia={self.nome_fantasia}, Categoria={self.categoria}, Status Aprovação={self.status_aprovacao})'
