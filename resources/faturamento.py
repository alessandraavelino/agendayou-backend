from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from flask_restful import fields
from helpers.database import db
from model.agendamento import Agendamento, agendamento_fields
from model.error import Error, error_campos
from model.faturamento import Faturamento, faturamento_fields
from sqlalchemy import func
parser = reqparse.RequestParser()
parser.add_argument('status', required=True)
parser.add_argument('nome_cliente', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('tipo_servico', required=True)
parser.add_argument('profissional', required=True)
parser.add_argument('valor', required=True)
parser.add_argument('horario', required=True)
parser.add_argument('parceiro_id', required=True)
parser.add_argument('pessoa_id', required=True)
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
            status = args['status']
            nome_cliente = args['nome_cliente']
            telefone = args['telefone']
            tipo_servico = args['tipo_servico']
            profissional = args['profissional']
            valor = args['valor']
            horario = args['horario']
            parceiro_id = args['parceiro_id']
            pessoa_id = args['pessoa_id']

            faturamento = Faturamento(status, nome_cliente, telefone, tipo_servico, profissional, horario, valor, parceiro_id, pessoa_id)

            db.session.add(faturamento)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204


class FaturamentoTotalResource(Resource):

    valor_field = {
        'valor': fields.Float(attribute='valor'),
        'presente': fields.Integer(attribute='presente'),
        'ausente': fields.Integer(attribute='ausente'),
    }

    @marshal_with(valor_field)
    def get(self, id_parceiro):
        current_app.logger.info(f"Get - Servico by ID: {id_parceiro}")

        valor = db.session.query(func.sum(Faturamento.valor)).scalar()
        presente = db.session.query(func.sum(Faturamento.status)).filter(Faturamento.status == 1).scalar()
        ausente = Faturamento.query.filter(Faturamento.status == 0).count()

        return {'valor': valor, 'presente': presente, 'ausente': ausente}, 200
    
class FaturamentoParceiroResource(Resource):

    @marshal_with(faturamento_fields)
    def get(self, parceiro_id):
        current_app.logger.info(f"Get - Servico by ID: {parceiro_id}")
        faturamento = Faturamento.query \
            .filter_by(parceiro_id=parceiro_id) \
            .all()

        if faturamento is None:
            # O serviço não foi encontrado
            erro = Error(404, f"Servico com ID {parceiro_id} não encontrado", "ServicoNotFound")
            return marshal(erro, error_campos), 404

        return faturamento, 200