from helpers.database import db
from flask_restful import fields
from model.servico import servico_fields, servico_agendamento_fields
agendamento_fields = {

    'id_agendamento': fields.Integer(attribute='id_agendamento'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'telefone': fields.String(attribute='telefone'),
    'servico': fields.Nested(servico_agendamento_fields)
}

class Agendamento(db.Model):

    __tablename__ = "tb_agendamento"
    
    id_agendamento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    
    servico = db.relationship("Servico", uselist=False)
    servico_id = db.Column(db.Integer, db.ForeignKey("tb_servico.id_servico"))

    def __init__(self, nome, email, telefone, servico):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.servico = servico

    def __repr__(self):
        return f'Agendamento(Nome={self.nome}, E-mail={self.email}, Telefone={self.telefone}, Servico={self.servico})'
