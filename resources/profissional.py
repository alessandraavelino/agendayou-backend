from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.profissional import Profissional, profissional_fields
from model.parceiro import Parceiro
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True) #c
parser.add_argument('cargo', required=True)
parser.add_argument('salario', required=True)
parser.add_argument('parceiro_id', required=True, type=int)

'''
  Classe Profissional (funcionário).
'''

class ProfissionalResource(Resource):

    @marshal_with(profissional_fields)
    def get(self):
        current_app.logger.info("Get - Parceiros")
        profissional = Profissional.query\
            .all()
        return profissional, 200

    def post(self):
        current_app.logger.info("Post - Parceiros")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            cargo = args['cargo']
            salario = args['salario']
            parceiro_id = args['parceiro_id']


            profissional = Profissional(nome, cargo, salario, parceiro_id)
            
            db.session.add(profissional)
            db.session.commit()

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

class ProfissionalUpdate(Resource):    
    def put(self, id_profissional):
        current_app.logger.info("Put - Profissional")
        try:
         # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Profissional: %s:" % args)
            #json

            nome = args['nome']
            cargo = args['cargo']
            salario = args['salario']
            parceiro_id = args['parceiro_id']
            
            profissional =Profissional.query \
                .filter_by(id_profissional=id_profissional) \
                .first()
            
            profissional.nome = nome
            profissional.cargo = cargo
            profissional.salario = salario
            profissional.parceiro_id = parceiro_id
            
            db.session.commit()
            
        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
class ProfissionalResourceById(Resource):

    @marshal_with(profissional_fields)
    def get(self, parceiro_id):
        current_app.logger.info(f"Get - Parceiro by ID: {parceiro_id}")
        profissional = Profissional.query \
            .filter_by(parceiro_id=parceiro_id) \
            .all()

        if profissional is None:
            # O serviço não foi encontrado
            erro = Error(404, f"Parceiro com ID {parceiro_id} não encontrado", "ParceiroNotFound")
            return marshal(erro, error_campos), 404

        return profissional, 200