from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db, migrate
from model.endereco import Endereco
from model.pessoa import Pessoa
from model.parceiro import Parceiro
from model.profissional import Profissional
from model.servico import Servico
from model.cliente import Cliente
from model.agendamento import Agendamento
from resources.login import LoginResource, EsqueciSenha

from resources.utils import GeracaoDeCodigo

from resources.parceiro import ParceiroResource
from resources.profissional import ProfissionalResource, ProfissionalUpdate
from resources.agendamento import AgendamentoResource
from resources.servico import ServicoResource
from resources.cliente import ClienteResource
# CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/agendayou"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate.init_app(app, db)

api = Api(app)

# Instâncias
endereco = Endereco("58255000", "Paraíba", "Belém", "Centro", "Rua São Joaquim")
# pessoa = Pessoa("Alê", "ale@mail.com", "12343", "23/01/2002", "123.456.789-80", "83996097405", endereco)
# print(pessoa)

# parceiro = Parceiro("dfdsf", "rtret", "Maria", "10/01/2001", "987.654.321-20", "40028922", endereco, "Mary Beautiful", "Beleza")
# print(parceiro)


servico = Servico("Fisioterapia", "Marcos", "65,OO", "2023-03-02 23:43:33")
print(servico)

profissional = Profissional("Maria", "Enfermeira", "2.000")
print(profissional)

cliente = Cliente("Alessandra", "ale@mail.com", "er", "545", "45dfg", "ewwkf", endereco)
print(cliente)

agendamento = Agendamento("Ale", "@", "083", servico)
print(agendamento)


# Resources
api.add_resource(ParceiroResource, '/parceiros')
api.add_resource(LoginResource, '/login')
api.add_resource(EsqueciSenha, '/esquecisenha')

api.add_resource(ProfissionalResource, '/profissional')
api.add_resource(ProfissionalUpdate, '/profissional/<int:id_profissional>')

api.add_resource(AgendamentoResource, '/agendamentos')
api.add_resource(ServicoResource, '/servicos')

api.add_resource(ClienteResource, '/clientes')
if __name__ == '__main__':
    app.run(debug=False)
