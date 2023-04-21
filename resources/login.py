from flask_restful import Resource, reqparse, current_app, marshal, marshal_with, Resource
from sqlalchemy import exc
import hashlib
from datetime import datetime
import smtplib

from helpers.database import db
from model.pessoa import Pessoa
from model.login import Login, login_campos
from model.error import Error, error_campos

from utils import GeracaoDeCodigo

from werkzeug.security import check_password_hash
import re

parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Campo e-mail é obrigatório.")
parser.add_argument('senha', required=True, help="Campo senha é obrigatório.")

codigoSenha = GeracaoDeCodigo()

class LoginResource(Resource):

    def post(self):
        current_app.logger.info("Post - Login")

        try:
            
            args = parser.parse_args()
            email = args['email']
            senha = args['senha']

            pessoa = Pessoa.query.filter_by(email=email).first()

            if pessoa and check_password_hash(pessoa.senha, senha):

                dataHoraLogin = datetime.now()
                hash = hashlib.sha1()
                hash.update(str(dataHoraLogin).encode("utf-8"))
                key = hash.hexdigest()
                login = Login(pessoa, dataHoraLogin, key)

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

class EsqueciSenha(Resource):
    
    
    def post(self):
        try:
            # JSON
            args = parser.parse_args()
            email_destinatario = args['email']

            corpo_email = "<p>"+"Codigo para atualizacao da senha: " + codigoSenha.GerarCodigo()+"</p>"
            
            msg = ""
            msg['Subject'] = "Codigo para Redefinicao da senha"
            msg['From']  = "agendayoficial@gmail.com"
            msg['To'] = email_destinatario
            password = "pcgbkkrsnuotykug" #Essa senha será gerada através de uma config lá do google
            msg.add_header("Content-Type", "text/html")
            msg.set_payload(corpo_email)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print("Email enviado com sucesso!!")

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return [{"message": "Convite enviado com sucesso!"}, 204]