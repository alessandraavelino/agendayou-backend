from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.servico import Servico, servico_fields
from model.cliente import Cliente
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('tipo_servico', required=True)
parser.add_argument('profissional', required=True)
parser.add_argument('valor', required=True)
parser.add_argument('horario', required=True)
'''
  Classe Servico.
'''

class ServicoResource(Resource):

    @marshal_with(servico_fields)
    def get(self):
        current_app.logger.info("Get - Servico")
        servico = Servico.query\
            .all()
        return servico, 200

    def post(self):
        current_app.logger.info("Post - Servico")
        try:
            #JSON
            args = parser.parse_args()
            tipo_servico = args['tipo_servico']
            profissional = args['profissional']
            valor = args['valor']
            horario = args['horario']

            servico = Servico(tipo_servico, profissional, valor, horario)

            db.session.add(servico)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204