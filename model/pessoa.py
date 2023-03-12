from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String

pessoa_fields = {

    'id_pessoa': fields.Integer(attribute='id_pessoa'),
    'nome': fields.String(attribute='nome'),
    'dt_nasc': fields.String(attribute='dt_nasc'),
    'cpf': fields.String(attribute='cpf'),
    'telefone': fields.String(attribute='telefone'),

}


class Pessoa(db.Model):

    __tablename__ = "tb_pessoa"

    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    dt_nasc = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)

    # Relacionamento com Endereço
    endereco = db.relationship("Endereco", uselist=False)
    parceiro = db.relationship("Parceiro", uselist=False)

    tipo_pessoa = db.Column('tipo_pessoa', String(50))
    __mapper_args__ = {'polymorphic_on': tipo_pessoa}


    def __init__(self, nome, dt_nasc, cpf, telefone, endereco):
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

    def __repr__(self):
        return f'Pessoa(Nome={self.nome}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereco={self.endereco})'
