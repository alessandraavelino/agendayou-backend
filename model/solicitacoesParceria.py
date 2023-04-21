from helpers.database import db
from flask_restful import fields

solicParceria_fields = {

    'id_solicitacao': fields.Integer(attribute='id_solicitacao'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'cnpj': fields.String(attribute='cnpj'),
    'qtdFuncion': fields.String(attribute='qtdFuncion'),
    'descricao': fields.String(attribute='descricao'),
}

class SolicitarParceria(db.Model):

    __tablename__ = "tb_solicParceria"
    
    id_solicitacao = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    qtdFuncion = db.Column(db.Integer(), nullable=False)
    descricao = db.Column(db.String(400), nullable=False)
    status = db.Column(db.String(20))

    parceiro = db.relationship("Parceiro", uselist=False)
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))

    def __init__(self, nome, email, cnpj, qtdFuncion, descricao, status=None):
        self.nome = nome
        self.email = email
        self.cnpj = cnpj
        self.qtdFuncion = qtdFuncion,
        self.descricao = descricao,
        self.status = status

    def __repr__(self):
        return f'Solicitação de Parceria(Nome={self.nome}, Email={self.email}, Cnpj={self.cnpj}, Qtd. funcionário={self.qtdFuncion}, Descrição={self.descricao}, Status={self.status})'
