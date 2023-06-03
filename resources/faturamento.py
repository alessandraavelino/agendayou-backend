from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.agendamento import Agendamento, agendamento_fields
from model.error import Error, error_campos
from model.faturamento import Faturamento, faturamento_fields
parser = reqparse.RequestParser()
parser.add_argument('faturamento', required=True)
parser.add_argument('status', required=True)
parser.add_argument('agendamento', type=dict,required=True)
'''
  Classe Agendamentos.
'''

class FaturamentoResource(Resource):

    @marshal_with(faturamento_fields)
    def get(self):
        current_app.logger.info("Get - Faturamentos")
        faturamento = Faturamento.query\
            .all()
        return faturamento, 200
    

    def post(self):
        current_app.logger.info("Post - Faturamentos")

        try:
            # JSON
            args = parser.parse_args()
            faturamento = args['faturamento']
            status = args['status']

            agendamentoArgs = args['agendamento']
            nome_cliente = agendamentoArgs['nome_cliente']
            telefone = agendamentoArgs['telefone']
            tipo_servico = agendamentoArgs['tipo_servico']
            profissional = agendamentoArgs['profissional']
            valor = agendamentoArgs['valor']
            horario = agendamentoArgs['horario']
            parceiro_id = agendamentoArgs['parceiro_id']
            pessoa_id = agendamentoArgs['pessoa_id']


            agendamento = Agendamento(nome_cliente, telefone, tipo_servico, profissional, horario, valor, parceiro_id, pessoa_id)
            faturamento = Faturamento(faturamento, status, agendamento)

            db.session.add(faturamento)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204

