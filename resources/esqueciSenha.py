from flask import Flask
from flask_restful import Resource, reqparse, current_app, marshal, marshal_with, abort
from sqlalchemy import exc
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

from helpers.database import db
from model.pessoa import Pessoa
from model.login import Login, login_campos
from model.error import Error, error_campos

from resources.utils import GerarCodigo
from werkzeug.security import check_password_hash, generate_password_hash
import re


parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Campo e-mail é obrigatório.")
codigo_gerado = GerarCodigo()

parserAtualizar = reqparse.RequestParser()
parserAtualizar.add_argument('codigo', required=True, help="Campo código é obrigatório.")
parserAtualizar.add_argument('nova_senha', required=True, help="Campo nova_senha é obrigatório.")


class EsqueciSenha(Resource):   
    def post(self):

        try:
            # JSON
            args = parser.parse_args()
            email_destinatario = args['email']
            
            corpo_email = "<p>" + "Codigo para atualizacao da senha: " + codigo_gerado + "</p>"
            
            msg = MIMEText(corpo_email, 'html')
            msg['Subject'] = "Codigo para Redefinicao da senha"
            msg['From']  = "agendayoficial@gmail.com"
            msg['To'] = email_destinatario
            password = "pcgbkkrsnuotykug" #Essa senha será gerada através de uma config lá do google
            msg.add_header("Content-Type", "text/html")
            
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

        return [{"message": "codigo enviado com sucesso!"}, 204]
    


class AtualizarSenhaResource(Resource):

    def put(self, email):
        current_app.logger.info("Put - Atualizar senha")

        try:
            # obter o código e a nova senha a partir dos argumentos
            args = parserAtualizar.parse_args()
            codigo = args['codigo']
            nova_senha = args['nova_senha']

            # obter a pessoa correspondente ao email
            pessoa = Pessoa.query.filter_by(email=email).first()           
            # se não encontrou a pessoa, abortar a requisição
            if not pessoa:
                 abort(404, message=f"pessoa com email: {email}, não encontrada")
            
            if codigo != codigo_gerado:
                abort(400, message="Código inválido")
            
            if len(nova_senha) < 8:
                abort(400, message="A senha deve conter pelos menos 8 caracteres")


            # atualizar a senha da pessoa
            pessoa.senha = generate_password_hash(nova_senha)

            # salvar as mudanças no banco de dados
            db.session.commit()

            # retornar a pessoa atualizada
            return [{"message": "senha atualizada com sucesso!"}, 204]

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao atualizar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        