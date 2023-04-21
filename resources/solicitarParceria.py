from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.error import Error, error_campos
from model.solicitacoesParceria import SolicitarParceria, solicParceria_fields
from flask import jsonify
parser = reqparse.RequestParser()
parser.add_argument('nome')
parser.add_argument('email')
parser.add_argument('cnpj')
parser.add_argument('qtdFunc')
parser.add_argument('descricao')
parser.add_argument('status')
'''
  Classe Solicitar Parceria.
'''

class SolicParceriaResource(Resource):

    @marshal_with(solicParceria_fields)
    def get(self):
        current_app.logger.info("Get - Parceiros")
        solicitacao = SolicitarParceria.query\
            .all()
        return solicitacao, 200
    
    def post(self):
        current_app.logger.info("Post - Solicitação")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            email = args['email']
            cnpj = args['cnpj']
            qtdFunc = args['qtdFunc']
            descricao = args['descricao']


            solicitacao = SolicitarParceria(nome, email, cnpj, qtdFunc, descricao)
            
            db.session.add(solicitacao)
            db.session.commit()

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
    
class StatusAprovacao(Resource): 
    def put(self, id_solicitacao):
        current_app.logger.info("Put - Solicitação de parceria")
        try:
         # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Solicitação: %s:" % args)
            #json

            status = args['status']
            solicitacao =SolicitarParceria.query \
                .filter_by(id_solicitacao=id_solicitacao) \
                .first()
            
            solicitacao.status = status
            
            db.session.commit()
            
        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, id_solicitacao):
        try:
            solicitacao = SolicitarParceria.query.filter_by(id_solicitacao=id_solicitacao).first()

            if solicitacao:
                db.session.delete(solicitacao)
                db.session.commit()
                return 200
            else:
                return 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
