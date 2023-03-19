from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.agendamento import Agendamento, agendamento_fields
from model.servico import Servico
from model.cliente import Cliente
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('email', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('servico', type=dict, required=True)

'''
  Classe Agendamentos.
'''

class AgendamentoResource(Resource):

    @marshal_with(agendamento_fields)
    def get(self):
        current_app.logger.info("Get - Agendamentos")
        agendamento = Agendamento.query\
            .all()
        return agendamento, 200

    def post(self):
        current_app.logger.info("Post - Agendamentos")
        try:
            #JSON
            args = parser.parse_args()
            nome = args['nome']
            email = args['email']
            telefone = args['telefone']

            servicoArgs = args['servico']
            tipo_servico = servicoArgs['tipo_servico']
            profissional = servicoArgs['profissional']
            valor = servicoArgs['valor']
            horario = servicoArgs['horario']

            servico = Servico(tipo_servico, profissional, valor, horario)

            agendamento = Agendamento(nome, email, telefone, servico)

            db.session.add(agendamento)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204