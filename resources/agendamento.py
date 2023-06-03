from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.agendamento import Agendamento, agendamento_fields
from model.servico import Servico
from model.cliente import Cliente
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome_cliente', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('tipo_servico', required=True)
parser.add_argument('profissional', required=True)
parser.add_argument('horario', required=True)
parser.add_argument('valor', required=True)
parser.add_argument('parceiro_id', type=int, required=True)
parser.add_argument('pessoa_id', type=int, required=True)

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
            # JSON
            args = parser.parse_args()
            nome_cliente = args['nome_cliente']
            telefone = args['telefone']
            tipo_servico = args['tipo_servico']
            profissional = args['profissional']
            horario = args['horario']
            valor = args['valor']
            parceiro_id = args['parceiro_id']
            pessoa_id = args['pessoa_id']
            
            agendamento = Agendamento(nome_cliente, telefone, tipo_servico, profissional, horario, valor, parceiro_id, pessoa_id)
            db.session.add(agendamento)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204
    
class AgendamentosParceiroResource(Resource):

    @marshal_with(agendamento_fields)
    def get(self, parceiro_id):
        current_app.logger.info(f"Get - Servico by ID: {parceiro_id}")
        agendamento = Agendamento.query \
            .filter_by(parceiro_id=parceiro_id) \
            .all()

        if agendamento is None:
            # O serviço não foi encontrado
            erro = Error(404, f"Servico com ID {parceiro_id} não encontrado", "ServicoNotFound")
            return marshal(erro, error_campos), 404

        return agendamento, 200