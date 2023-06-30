from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.administrador import Administrador, administrador_fields
from model.endereco import Endereco
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Email é um campo obrigatório.")
parser.add_argument('senha', required=True, help="Senha é campo obrigatório.")
parser.add_argument('nome', required=True)
parser.add_argument('dt_nasc', required=True)
parser.add_argument('cpf', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('endereco', type=dict, required=True)

'''
  Classe Administrador.
'''

class AdministradorResource(Resource):

    @marshal_with(administrador_fields)
    def get(self):
        current_app.logger.info("Get - Administrador")
        administrador = Administrador.query\
            .all()
        return administrador, 200

    def post(self):
        current_app.logger.info("Post - Administrador")
        try:
            # JSON
            args = parser.parse_args()
            email = args['email']
            senha = args['senha']
            nome = args['nome']
            dt_nasc = args['dt_nasc']
            cpf = args['cpf']
            telefone = args['telefone']

            enderecoArgs = args['endereco']
            cep = enderecoArgs['cep']
            estado = enderecoArgs['estado']
            cidade = enderecoArgs['cidade']
            bairro = enderecoArgs['bairro']
            rua = enderecoArgs['rua']

            endereco = Endereco(cep, estado, cidade, bairro, rua)
            
    
            administrador = Administrador(nome=nome, dt_nasc=dt_nasc, cpf=cpf, telefone=telefone, endereco=endereco, email=email, senha=senha)

            db.session.add(administrador)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204