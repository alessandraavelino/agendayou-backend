from helpers.database import db
from flask_restful import fields
from datetime import datetime

agendamento_fields = {

    'id_agendamento': fields.Integer(attribute='id_agendamento'),
    'nome': fields.String(attribute='nome'),
    'telefone': fields.String(attribute='telefone'),
    'profissional': fields.String(attribute='profissional'),
    'horario': fields.String(attribute='horario'),
    'servico': fields.String(attribute='servico'),
    'parceiro_id':  fields.Integer(attribute='parceiro_id')
    
}

class Agendamento(db.Model):

    __tablename__ = "tb_agendamento"
    
    id_agendamento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    profissional = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime(50), default=datetime.utcnow)
    servico = db.Column(db.String(50), nullable=False)

    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, nome, telefone, profissional, horario, servico, parceiro_id):
        self.nome = nome
        self.telefone = telefone
        self.profissional = profissional
        self.set_horario(horario)
        self.servico = servico
        self.parceiro_id = parceiro_id
    
    def set_horario(self, horario):
        data_hora = horario
        format_hora = datetime.strptime(data_hora, '%Y-%m-%d %H:%M')
        self.horario = format_hora

    def __repr__(self):
        return f'Agendamento(Nome={self.nome}, Telefone={self.telefone}, Horário={self.horario}, Servico={self.servico})'
