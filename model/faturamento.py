from helpers.database import db
from flask_restful import fields
from datetime import datetime
from model.agendamento import agendamento_fields

faturamento_fields = {
    'id_faturamento': fields.Integer(attribute='id_faturamento'),
    'faturamento': fields.String(attribute='nome_cliente'),
    'status': fields.String(attribute='status'),
    'agendamento': fields.Nested(agendamento_fields)
}

class Faturamento(db.Model):

    __tablename__ = "tb_faturamento"
    
    id_faturamento = db.Column(db.Integer, primary_key=True)
    faturamento = db.Column(db.String(50), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    # Relacionamento com Endereço
    agendamento = db.relationship("Agendamento", uselist=False)
    agendamento_id = db.Column(db.Integer, db.ForeignKey("tb_agendamento.id_agendamento"))


    def __init__(self, faturamento, status, agendamento, ):
        self.faturamento = faturamento
        self.status = status
        self.agendamento = agendamento

    def __repr__(self):
        return f'Agendamento(Cliente={self.Faturamento}, Status={self.status}, Agendamento={self.agendamento})'
