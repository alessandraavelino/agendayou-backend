from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.pessoa import Pessoa, pessoa_fields
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('foto')
parser.add_argument('email', required=True)
parser.add_argument('dt_nasc', required=True)
parser.add_argument('cpf', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('endereco', required=True)
parser.add_argument('endereco', type=dict, required=True)


'''
  Classe Pessoa.
'''

class PessoaResource(Resource):

    @marshal_with(pessoa_fields)
    def get(self):
        current_app.logger.info("Get - Parceiros")
        pessoa = Pessoa.query\
            .all()
        return pessoa, 200

# class ProfissionalUpdate(Resource):    
#     def put(self, id_profissional):
#         current_app.logger.info("Put - Profissional")
#         try:
#          # Parser JSON
#             args = parser.parse_args()
#             current_app.logger.info("Profissional: %s:" % args)
#             #json

#             nome = args['nome']
#             cargo = args['cargo']
#             salario = args['salario']

            
#             profissional =Profissional.query \
#                 .filter_by(id_profissional=id_profissional) \
#                 .first()
            
#             profissional.nome = nome
#             profissional.cargo = cargo
#             profissional.salario = salario
            
#             db.session.commit()
            
#         except exc.SQLAlchemyError:
#             current_app.logger.error("Exceção")

#         return 204

class PessoaByIdResource(Resource):

    @marshal_with(pessoa_fields)
    def get(self, id_pessoa):
        current_app.logger.info(f"Get - Servico by ID: {id_pessoa}")
        pessoa = Pessoa.query \
            .filter_by(id_pessoa=id_pessoa) \
            .all()

        if pessoa is None:
            # O serviço não foi encontrado
            erro = Error(404, f"Pessoa com ID {id_pessoa} não encontrado", "pessoaNotFound")
            return marshal(erro, error_campos), 404

        return pessoa, 200
    
    def put(self, id_pessoa):
        current_app.logger.info("Put - Pessoa")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Pessoa: %s:" % args)

            # Obtenha os campos a serem atualizados do JSON
            foto = args['foto']
            nome = args['nome']
            email = args['email']
            dt_nasc = args['dt_nasc']
            cpf = args['cpf']
            telefone = args['telefone']

            # Obtenha o objeto Pessoa a ser atualizado
            pessoa = Pessoa.query.get(id_pessoa)
            
            if pessoa:
                # Atualize os campos da Pessoa
                pessoa.nome = nome
                pessoa.foto = foto
                pessoa.email = email
                pessoa.dt_nasc = dt_nasc
                pessoa.cpf = cpf
                pessoa.telefone = telefone

                # Atualize o Endereco da Pessoa
                endereco = pessoa.endereco
                if endereco:
                    # Atualize os campos do Endereco
                    endereco.bairro = args['endereco']['bairro']
                    endereco.cidade = args['endereco']['cidade']
                    endereco.estado = args['endereco']['estado']
                    endereco.rua = args['endereco']['rua']

            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204