from helpers.database import db
from flask_restful import fields
from datetime import datetime
from model.agendamento import agendamento_fields

faturamento_fields = {
    'id_faturamento': fields.Integer(attribute='id_faturamento'),
    'status': fields.Integer(attribute='status'),
    'nome_cliente': fields.String(attribute='nome_cliente'),
    'telefone': fields.String(attribute='telefone'),
    'tipo_servico': fields.String(attribute='tipo_servico'),
    'profissional': fields.String(attribute='profissional'),
    'horario': fields.String(attribute=lambda x: x.horario.strftime('%d/%m/%Y %H:%M')),
    'valor': fields.Float(attribute='valor'),
    'parceiro_id': fields.Integer(attribute='parceiro_id'),
    'pessoa_id': fields.Integer(attribute='pessoa_id'),
}

class Faturamento(db.Model):

    __tablename__ = "tb_faturamento"
    
    id_faturamento = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, nullable=False)
    nome_cliente = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    profissional = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    horario = db.Column(db.DateTime, default=datetime.now)

    # Relacionamento com Endereço
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, status, nome_cliente, telefone, tipo_servico, profissional, horario, valor, parceiro_id, pessoa_id):
        self.status = status
        self.nome_cliente = nome_cliente
        self.telefone = telefone
        self.tipo_servico = tipo_servico
        self.profissional = profissional
        self.set_horario(horario)
        self.valor = valor
        self.parceiro_id = parceiro_id,
        self.pessoa_id = pessoa_id
    
    def set_horario(self, horario):
        dt_format = datetime.strptime(horario, '%d/%m/%Y %H:%M')
        self.horario = dt_format

    def __repr__(self):
        return f'Agendamento(Status={self.status}, Agendamento={self.agendamento})'

