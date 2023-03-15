from flask_restful import Resource, reqparse, current_app, marshal, marshal_with, Resource
from sqlalchemy import exc
import hashlib
from datetime import datetime

from helpers.database import db
from model.pessoa import Pessoa
from model.login import Login, login_campos
from model.error import Error, error_campos

parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Campo e-mail é obrigatório.")
parser.add_argument('senha', required=True, help="Campo senha é obrigatório.")


class LoginResource(Resource):

    def post(self):
        current_app.logger.info("Post - Login")

        try:
            # JSON
            args = parser.parse_args()
            email = args['email']
            senha = args['senha']
            # TODO - Adicionar consulta ao banco de dados.
            # Consultar se exite o pessoa através do e-mail e senha
            pessoa = Pessoa.query.filter_by(email=email, senha=senha).first()
            # db.select(Pessoa).filter_by(email=email, senha=senha).first()
            # db.session.query(Pessoa).filter(Pessoa.email == email, Pessoa.senha == senha)

            if (pessoa is not None):
                dataHoraLogin = datetime.now()
                hash = hashlib.sha1()
                hash.update(str(dataHoraLogin).encode("utf-8"))
                key = hash.hexdigest()
                login = Login(pessoa, dataHoraLogin, key)

                # Criação do Login.
                db.session.add(login)
                db.session.commit()

                return (marshal(login, login_campos), 200)

            else:
                error = Error(2, "E-mail ou senha inválidos", "")
                return (marshal(error, error_campos), 401)

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
