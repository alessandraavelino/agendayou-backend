from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.suporte import Suporte, suporte_fields
from model.error import Error, error_campos
from flask import jsonify

parser = reqparse.RequestParser()

parser.add_argument('descricao', required=True)
parser.add_argument('pessoa_id', required=True)

'''
  Classe Suporte.
'''

class SuporteResource(Resource):

    @marshal_with(suporte_fields)
    def get(self):
        current_app.logger.info("Get - Suporte")
        suporte = Suporte.query\
            .all()
        return suporte, 200

    def post(self):
        current_app.logger.info("Post - Servico")
        try:
            #JSON
            args = parser.parse_args()
            descricao = args['descricao']
            pessoa_id = args['pessoa_id']

            suporte = Suporte(descricao, pessoa_id)

            db.session.add(suporte)
            db.session.commit()
            
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204

class SuporteResourceById(Resource):
    def delete(self, id_suporte):
        try:
            suporte = Suporte.query.filter_by(id_suporte=id_suporte).first()
            
            if suporte:

                db.session.delete(suporte)
                db.session.commit()
                
                return 204
            else:
                return 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

