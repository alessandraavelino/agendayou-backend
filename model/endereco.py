from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String

endereco_fields = {

    'id_endereco': fields.Integer(attribute='id_endereco'),
    'cep': fields.String(attribute='cep'),
    'estado': fields.String(attribute='estado'),
    'cidade': fields.String(attribute='cidade'),
    'bairro': fields.String(attribute='bairro'),
    'rua': fields.String(attribute='rua'),
    'numero': fields.String(attribute='numero'),
}

class Endereco(db.Model):

    __tablename__ = "tb_endereco"

    id_endereco = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(8), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)

    # Relacionamento com Pessoa
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, cep, estado, cidade, bairro, rua, numero):
        self.cep = cep
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero

    def __repr__(self):
        return f'Endereço(CEP={self.cep}, Estado={self.estado}, Cidade={self.cidade}, Bairro={self.bairro}, Rua={self.rua}, Número={self.numero})'
