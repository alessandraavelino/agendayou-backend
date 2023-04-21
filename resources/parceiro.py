from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.parceiro import Parceiro, parceiro_fields
from model.endereco import Endereco
from model.error import Error, error_campos
parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Email é um campo obrigatório.")
parser.add_argument('senha', required=True, help="Senha é campo obrigatório.")
parser.add_argument('nome', required=True)
parser.add_argument('dt_nasc', required=True) #checada de data
parser.add_argument('cpf', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('endereco', type=dict, required=True)
parser.add_argument('nome_fantasia', required=True)
parser.add_argument('categoria', required=True)

'''
  Classe Funcionário.
'''

class ParceiroResource(Resource):

    @marshal_with(parceiro_fields)
    def get(self):
        current_app.logger.info("Get - Parceiros")
        parceiro = Parceiro.query\
            .all()
        return parceiro, 200

    def post(self):
        current_app.logger.info("Post - Parceiros")
        try:
            # JSON
            args = parser.parse_args()
            email = args['email']
            senha = args['senha']
            nome = args['nome']
            dt_nasc = args['dt_nasc']
            cpf = args['cpf']
            telefone = args['telefone']
            nome_fantasia = args['nome_fantasia']
            categoria = args['categoria']

            parceiro = Parceiro(nome=nome, dt_nasc=dt_nasc, cpf=cpf, telefone=telefone, nome_fantasia=nome_fantasia, categoria=categoria, email=email, senha=senha)

            db.session.add(parceiro)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204