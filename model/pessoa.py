from helpers.database import db
from flask_restful import fields
from sqlalchemy.types import String
from model.endereco import endereco_fields
from werkzeug.security import generate_password_hash
pessoa_fields = {

    'id_pessoa': fields.Integer(attribute='id_pessoa'),
    'foto': fields.String(attribute='foto'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'senha': fields.String(attribute='senha'),
    'dt_nasc': fields.String(attribute='dt_nasc'),
    'cpf': fields.String(attribute='cpf'),
    'telefone': fields.String(attribute='telefone'),
    'tipo_pessoa': fields.String(attribute='tipo_pessoa'),
    'endereco': fields.Nested(endereco_fields),

}


class Pessoa(db.Model):

    __tablename__ = "tb_pessoa"

    id_pessoa = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(1000))
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(1000), nullable=False)
    dt_nasc = db.Column(db.String(20), nullable=True)
    cpf = db.Column(db.String(20), nullable=True, unique=True)
    telefone = db.Column(db.String(20), nullable=True)

    # Relacionamento com Endereço
    endereco = db.relationship("Endereco", uselist=False)
    parceiro = db.relationship("Parceiro", uselist=False)

    tipo_pessoa = db.Column('tipo_pessoa', String(50))
    __mapper_args__ = {'polymorphic_on': tipo_pessoa}

    agendamentos = db.relationship("Agendamento", cascade="all, delete")


    def __init__(self, nome, email, senha, dt_nasc, cpf, telefone, endereco, foto=None):
        self.foto = None
        self.nome = nome
        self.email = email
        self.set_senha(senha)
        self.dt_nasc = dt_nasc
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha, method='sha256')



    def __repr__(self):
        return f'Pessoa(Nome={self.nome}, E-mail={self.email}, Senha={self.senha}, Data de Nascimento={self.dt_nasc}, CPF={self.cpf}, Telefone={self.telefone}, Endereco={self.endereco}, Tipo de Pessoa={self.tipo_pessoa})'
