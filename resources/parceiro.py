from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.parceiro import Parceiro, parceiro_fields
from model.endereco import Endereco
from model.error import Error, error_campos
from email.mime.text import MIMEText
from flask import jsonify, abort
import smtplib
parser = reqparse.RequestParser()
parser.add_argument('email', required=True, help="Email é um campo obrigatório.")
parser.add_argument('senha', required=True, help="Senha é campo obrigatório.")
parser.add_argument('nome', required=True)
parser.add_argument('nome_fantasia', required=True)
parser.add_argument('categoria', required=True)

'''
  Classe Funcionário.
'''

class ParceiroResource(Resource):

    @marshal_with(parceiro_fields)
    def get(self):
        current_app.logger.info("Get - Parceiros")
        parceiro = Parceiro.query\
            .all()
        return parceiro, 200

    def post(self):
        current_app.logger.info("Post - Parceiros")
        try:
            # JSON
            args = parser.parse_args()
            email = args['email']
            senha = args['senha']
            nome = args['nome']
            nome_fantasia = args['nome_fantasia']
            categoria = args['categoria']

            parceiro = Parceiro(nome=nome,  nome_fantasia=nome_fantasia, categoria=categoria, email=email, senha=senha)

            email_destinatario = email
            
            corpo_email = f"""
                            <h5>Solicitação de Parceria - AgendaYOU</h5>

                            "<p>Prezado, {nome}/p>

                            <p>É com grande satisfação que informamos que a sua 
                            solicitação de parceria foi aprovada. Estamos ansiosos 
                            para trabalhar juntos e desenvolver uma relação de 
                            sucesso mútuo.</p>

                            <p>Estamos confiantes de que essa parceria será benéfica
                            para ambas as partes e que juntos poderemos alcançar 
                            grandes conquistas. Agradecemos pelo interesse em nossa 
                            empresa e esperamos contribuir para o crescimento de seu 
                            negócio</p>

                            <p>Segue seu e-mail e senha para acessar o sistema</p>
                            <span><strong>E-mail: </strong><span>{email}</span>
                            <span><strong>E-mail: </strong><span>{senha}</span>

                            <p>Atenciosamente,</p>
                            <p>AgendaYOU</p>
                        """
            
            msg = MIMEText(corpo_email, 'html')
            msg['Subject'] = "Feedback Parceria - AgendaYOU"
            msg['From']  = "agendayoficial@gmail.com"
            msg['To'] = email_destinatario
            password = "pcgbkkrsnuotykug" #Essa senha será gerada através de uma config lá do google
            msg.add_header("Content-Type", "text/html")
            
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            s.login(msg['From'], password)
            #s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print("Email enviado com sucesso!!")
            
            db.session.add(parceiro)
            db.session.commit()
            
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500
        
        return 204
    

    
    
class DeletarParceiro(Resource):
    @marshal_with(parceiro_fields)
    def delete(self, id_parceiro):
        try:
            parceiro = Parceiro.query.filter_by(id_parceiro=id_parceiro).first()

            if parceiro:
                
                db.session.delete(parceiro)
                db.session.commit()

                return 204
            else:
                abort(404)  # Aborta a solicitação com o código de status 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

