from helpers.database import db
from flask_restful import fields

categoria_fields = {

    'id_categoria': fields.Integer(attribute='id_categoria'),
    'categoria': fields.String(attribute='categoria')

}

class Categoria(db.Model):

    __tablename__ = "tb_categoria"
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, categoria):
        self.categoria = categoria

    def __repr__(self):
        return f'Agendamento(Categoria={self.nome})'
