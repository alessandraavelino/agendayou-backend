from helpers.database import db
from flask_restful import fields

solicParceria_fields = {

    'id_solicitacao': fields.Integer(attribute='id_solicitacao'),
    'nome': fields.String(attribute='nome'),
    'nome_fantasia': fields.String(attribute='nome_fantasia'),
    'email': fields.String(attribute='email'),
    'categoria': fields.String(attribute='categoria'),
    'cnpj': fields.String(attribute='cnpj'),
    'qtdFuncion': fields.String(attribute='qtdFuncion'),
    'descricao': fields.String(attribute='descricao'),
}

class SolicitarParceria(db.Model):

    __tablename__ = "tb_solicParceria"
    
    id_solicitacao = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    nome_fantasia = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)

    qtdFuncion = db.Column(db.Integer(), nullable=False)
    descricao = db.Column(db.String(400), nullable=False)

    parceiro = db.relationship("Parceiro", uselist=False)
    parceiro_id = db.Column(db.Integer, db.ForeignKey("tb_parceiro.id_parceiro"))
    

    def __init__(self, nome, nome_fantasia, email, cnpj, categoria, qtdFuncion, descricao):
        self.nome = nome
        self.nome_fantasia = nome_fantasia 
        self.email = email
        self.cnpj = cnpj
        self.categoria = categoria
        self.qtdFuncion = qtdFuncion,
        self.descricao = descricao

    def __repr__(self):
        return f'Solicitação de Parceria(Nome={self.nome}, Nome Fantasia={self.nome_fantasia}, Email={self.email}, Cnpj={self.cnpj}, Qtd. funcionário={self.qtdFuncion}, Descrição={self.descricao})'
