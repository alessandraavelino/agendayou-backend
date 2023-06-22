from helpers.database import db
from flask_restful import fields

profissional_fields = {

    'id_profissional': fields.Integer(attribute='id_profissional'),
    'nome': fields.String(attribute='nome'),
    'cargo': fields.String(attribute='cargo'),
    'salario': fields.String(attribute='salario'),
    'parceiro_id': fields.Integer(attribute='parceiro_id')
}

class Profissional(db.Model):

    __tablename__ = "tb_profissional"
    
    id_profissional = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.String(10), nullable=True)

    parceiro = db.relationship("Parceiro", uselist=False)
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, nome, cargo, salario, parceiro_id):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        self.parceiro_id = parceiro_id

    def __repr__(self):
        return f'Profissional(Nome={self.nome}, Cargo={self.cargo}, Salário={self.salario},Parceiro_id={self.parceiro_id} )'
