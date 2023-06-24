from helpers.database import db
from flask_restful import fields
from datetime import datetime
from sqlalchemy.types import String

servico_fields = {
    'id_servico': fields.Integer(attribute='id_servico'),
    'nome_parceiro': fields.String(attribute='nome_parceiro'),
    'tipo_servico': fields.String(attribute='tipo_servico'),
    'profissional': fields.String(attribute='profissional'),
    'valor': fields.Float(attribute='valor'),
    'horario': fields.String(attribute=lambda x: x.horario.strftime('%d/%m/%Y %H:%M')),
    'categoria': fields.String(attribute='categoria'),
    'parceiro_id': fields.Integer(attribute='parceiro_id'),
    'foto_parceiro': fields.String(attribute=lambda x: x.parceiro.foto)
}

class Servico(db.Model):
    __tablename__ = "tb_servico"

    id_servico = db.Column(db.Integer, primary_key=True)
    nome_parceiro = db.Column(db.String(50), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    profissional = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    horario = db.Column(db.DateTime, default=datetime.now)
    categoria = db.Column(db.String(50), nullable=False)

    # Relacionamento com Parceiro
    parceiro = db.relationship("Parceiro", uselist=False, backref="servicos")
    categoria_id = db.Column(db.Integer, db.ForeignKey("tb_categoria.id_categoria"))
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, nome_parceiro, tipo_servico, profissional, valor, horario, categoria, parceiro_id):
        self.nome_parceiro = nome_parceiro
        self.tipo_servico = tipo_servico
        self.profissional = profissional
        self.valor = valor
        self.categoria = categoria
        self.set_horario(horario)
        self.parceiro_id = parceiro_id

    def set_horario(self, horario):
        dt_format = datetime.strptime(horario, '%d/%m/%Y %H:%M')
        self.horario = dt_format

    def __repr__(self):
        return f'Serviço("Parceiro={self.parceiro}, Tipo de Serviço={self.tipo_servico}, Profissional={self.profissional}, Valor={self.valor}, Horário={self.horario})'
