from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc
from helpers.database import db
from model.error import Error, error_campos
from model.solicitacoesParceria import SolicitarParceria, solicParceria_fields
from flask import jsonify
import smtplib
from flask import make_response

from email.mime.text import MIMEText
parser = reqparse.RequestParser()
parser.add_argument('nome')
parser.add_argument('nome_fantasia')
parser.add_argument('categoria')
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
            nome_fantasia = args['nome_fantasia']
            categoria = args['categoria']
            email = args['email']
            cnpj = args['cnpj']
            qtdFunc = args['qtdFunc']
            descricao = args['descricao']


            solicitacao = SolicitarParceria(nome, nome_fantasia, email, cnpj, categoria, qtdFunc, descricao)
            
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
    
    
    def delete(self, id_solicitacao, email):
        try:
            solicitacao = SolicitarParceria.query.filter_by(id_solicitacao=id_solicitacao).first()
            
            if solicitacao:
                email_destinatario = email
            
                corpo_email = """
                                <h5>Solicitação de Parceria - AgendaYOU</h5>

                                "<p>Gostaríamos de agradecer pelo interesse em"
                                estabelecer uma parceria conosco. Analisamos
                                cuidadosamente sua proposta e apreciamos o
                                tempo e esforço que você investiu em nos 
                                apresentar sua empresa e seus objetivos.</p>

                                <p>Após uma análise minuciosa, no entanto, 
                                decidimos que, neste momento, não estamos 
                                em posição de aceitar sua proposta de parceria. 
                                Queremos que saiba que isso não reflete sobre a 
                                qualidade de sua empresa ou de seus serviços, 
                                mas sim em nossa atual estratégia de negócios.</p>

                                <p>Queremos expressar nossa gratidão pela sua proposta 
                                e esperamos que possamos continuar em contato no futuro. 
                                Agradecemos novamente pela sua consideração e desejamos 
                                o melhor para o sucesso contínuo de sua empresa.</p>

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
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
                print("Email enviado com sucesso!!")

                db.session.delete(solicitacao)
                db.session.commit()
                
                return 204
            else:
                return 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
class StatusAprovado(Resource):
    def delete(self, email):
        try:
            solicitacao = SolicitarParceria.query.filter_by(email=email).first()
            print("solicitacao", solicitacao)
            
            if solicitacao:
                db.session.delete(solicitacao)
                db.session.commit()
                
                return 204
            else:
                return 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
