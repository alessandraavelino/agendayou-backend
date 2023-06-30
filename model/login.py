from datetime import datetime

from helpers.database import db
from model.pessoa import Pessoa, pessoa_fields
from model.parceiro import Parceiro, parceiro_fields
from model.administrador import Administrador, administrador_fields
from flask_restful import fields

login_campos = {
    'id': fields.Integer(attribute='id'),
    'pessoa': fields.Nested(pessoa_fields),
    'datahora': fields.String(attribute='datahora'),
    'key': fields.String(attribute='key'),
    'parceiro': fields.Nested(parceiro_fields),
}


class Login(db.Model):

    __tablename__ = 'tb_login'

    id = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))
    datahora = db.Column(db.DateTime, default=datetime.now)

    key = db.Column(db.String(40))

    pessoa = db.relationship("Pessoa", uselist=False)
    parceiro = db.relationship("Parceiro", uselist=False)

    def __init__(self, pessoa: Pessoa, datahora, key, parceiro: Parceiro):
        self.datahora = datahora
        self.pessoa = pessoa
        self.key = key
        self.parceiro = parceiro

    def __repr__(self):
        return f'Login(Horário={self.datahora})'