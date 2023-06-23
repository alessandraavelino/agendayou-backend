from helpers.database import db
from flask_restful import fields
from datetime import datetime
from sqlalchemy.types import String

suporte_fields = {
    'id_suporte': fields.Integer(attribute='id_suporte'),
    'descricao': fields.String(attribute='descricao'),
    'pessoa_id': fields.String(attribute='pessoa_id'),
}

class Suporte(db.Model):
    __tablename__ = "tb_suporte"

    id_suporte = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(500), nullable=False)

    # Relacionamento com Parceiro
    pessoa = db.relationship("Pessoa", uselist=False, backref="suporte")
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, descricao, pessoa_id):
        self.descricao = descricao
        self.pessoa_id = pessoa_id


    def __repr__(self):
        return f'Serviço("descricao={self.descricao}'
