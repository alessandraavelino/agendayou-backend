from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.servico import Servico, servico_fields
from model.cliente import Cliente
from model.error import Error, error_campos
from flask import jsonify
parser = reqparse.RequestParser()
parser.add_argument('tipo_servico', required=True)
parser.add_argument('nome_parceiro', required=True)
parser.add_argument('profissional', required=True)
parser.add_argument('valor', required=True)
parser.add_argument('horario', required=True)
parser.add_argument('categoria', required=True)
parser.add_argument('parceiro_id', type=int, required=True)

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
            nome_parceiro = args['nome_parceiro']
            tipo_servico = args['tipo_servico']
            profissional = args['profissional']
            valor = args['valor']
            horario = args['horario']
            categoria = args['categoria']
            parceiro_id = args['parceiro_id']

            servico = Servico(nome_parceiro, tipo_servico, profissional, valor, horario, categoria, parceiro_id)

            db.session.add(servico)
            db.session.commit()
            
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204
    
class ServicoResourceById(Resource):

    @marshal_with(servico_fields)
    def get(self, parceiro_id):
        current_app.logger.info(f"Get - Servico by ID: {parceiro_id}")
        servico = Servico.query \
            .filter_by(parceiro_id=parceiro_id) \
            .all()

        if servico is None:
            # O serviço não foi encontrado
            erro = Error(404, f"Servico com ID {parceiro_id} não encontrado", "ServicoNotFound")
            return marshal(erro, error_campos), 404

        return servico, 200

    
class ServicoUpdateById(Resource):
    def put(self, id_servico):
        current_app.logger.info("Put - Serviço")
        try:
         # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Serviço: %s:" % args)
            #json

            tipo_servico = args['tipo_servico']
            profissional = args['profissional']
            horario = args['horario']
            valor = args['valor']

            
            servico =Servico.query \
                .filter_by(id_servico=id_servico) \
                .first()
            
            servico.tipo_servico = tipo_servico
            servico.profissional = profissional
            servico.valor = valor
            servico.horario = horario
            
            db.session.commit()
            
        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, id_servico):
        try:
            servico = Servico.query.filter_by(id_servico=id_servico).first()
            
            if servico:

                db.session.delete(servico)
                db.session.commit()
                
                return 204
            else:
                return 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

