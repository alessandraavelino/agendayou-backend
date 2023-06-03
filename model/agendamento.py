from helpers.database import db
from flask_restful import fields
from datetime import datetime

agendamento_fields = {
    'id_agendamento': fields.Integer(attribute='id_agendamento'),
    'nome_cliente': fields.String(attribute='nome_cliente'),
    'telefone': fields.String(attribute='telefone'),
    'tipo_servico': fields.String(attribute='tipo_servico'),
    'profissional': fields.String(attribute='profissional'),
    'horario': fields.String(attribute=lambda x: x.horario.strftime('%d/%m/%Y %H:%M')),
    'parceiro_id': fields.Integer(attribute='parceiro_id'),
    'pessoa_id': fields.Integer(attribute='pessoa_id'),
}

class Agendamento(db.Model):

    __tablename__ = "tb_agendamento"
    
    id_agendamento = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    profissional = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime, default=datetime.now)

    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id_pessoa"))

    def __init__(self, nome_cliente, telefone, tipo_servico, profissional, horario, valor, parceiro_id, pessoa_id):
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
        return f'Agendamento(Cliente={self.nome_cliente}, Telefone={self.telefone}, Tipo Serviço={self.tipo_servico}, Profissional={self.profissional}, Horário={self.horario}, Valor={self.valor})'
