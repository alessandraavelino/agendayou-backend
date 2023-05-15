from helpers.database import db
from flask_restful import fields
from datetime import datetime
from sqlalchemy.types import String

servico_fields = {

    'id_servico': fields.Integer(attribute='id_servico'),
    'nome_parceiro': fields.String(attribute='nome_parceiro'),
    'tipo_servico': fields.String(attribute='tipo_servico'),
    'profissional': fields.String(attribute='profissional'),
    'valor': fields.String(attribute='valor'),
    'horario': fields.String(attribute='horario'),
    'categoria': fields.String(attribute='categoria')

}

servico_agendamento_fields = {

    'id_servico': fields.Integer(attribute='id_servico'),
    'tipo_servico': fields.String(attribute='tipo_servico'),
    'profissional': fields.String(attribute='profissional'),
    'horario': fields.String(attribute='horario')

}

class Servico(db.Model):

    __tablename__ = "tb_servico"

    id_servico = db.Column(db.Integer, primary_key=True)
    nome_parceiro = db.Column(db.String(50), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    profissional = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime(50), nullable=False, default=datetime.utcnow)
    categoria = db.Column(db.String(50), nullable=False)
    
    # Relacionamento com Parceiro
    parceiro = db.relationship("Parceiro", uselist=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("tb_categoria.id_categoria"))
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))
 
    def __init__(self, nome_parceiro, tipo_servico, profissional, valor, horario1, horario2, horario3, categoria):
        self.nome_parceiro = nome_parceiro
        self.tipo_servico = tipo_servico
        self.profissional = profissional
        self.valor = valor
        self.categoria = categoria
        self.set_horario(horario1)
        self.set_horario(horario2)
        self.set_horario(horario3)

    def set_horario(self, horario):
        data_hora = horario
        format_hora = datetime.strptime(data_hora, '%Y-%m-%d %H:%M:%S')
        self.horario = format_hora

    def __repr__(self):
        return f'Serviço("Parceiro={self.parceiro}, Tipo de Serviço={self.tipo_servico}, Profissional={self.profissional}, Valor={self.valor}, Horário={self.horario})'
