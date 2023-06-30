from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.categoria import Categoria, categoria_fields
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('categoria', required=True)

'''
  Classe Categoria.
'''

class CategoriaResource(Resource):

    @marshal_with(categoria_fields)
    def get(self):
        current_app.logger.info("Get - Categoria")
        categoria = Categoria.query\
            .all()
        return categoria, 200

    def post(self):
        current_app.logger.info("Post - Categoria")
        try:
            #JSON
            args = parser.parse_args()
            categoria = args['categoria']

            categoria = Categoria(categoria)

            db.session.add(categoria)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204