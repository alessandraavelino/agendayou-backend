from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db, migrate
from model.endereco import Endereco

from model.parceiro import Parceiro
from model.profissional import Profissional
from model.servico import Servico
from model.cliente import Cliente
from model.agendamento import Agendamento
from model.solicitacoesParceria import SolicitarParceria
from resources.pessoa import PessoaResource, PessoaByIdResource
from resources.esqueciSenha import AtualizarSenhaResource, EsqueciSenha
from resources.login import LoginResource, LogoutResource
from resources.parceiro import DeletarParceiro, ParceiroResource
from resources.profissional import ProfissionalResource, ProfissionalResourceById, ProfissionalUpdate
from resources.agendamento import AgendamentoResource, AgendamentosParceiroResource, AgendamentosByIdResource, AgendamentosPessoaResource
from resources.servico import ServicoResource, ServicoResourceById, ServicoUpdateById
from resources.cliente import ClienteResource
from resources.solicitarParceria import StatusAprovado, StatusAtivo
from resources.solicitarParceria import SolicParceriaResource
from resources.solicitarParceria import StatusAprovacao
from resources.faturamento import FaturamentoResource, FaturamentoTotalResource, FaturamentoParceiroResource
from resources.administrador import AdministradorResource
from resources.categoria import CategoriaResource
# CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/agendayou"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate.init_app(app, db)

api = Api(app)

# Resources
api.add_resource(DeletarParceiro, '/parceiros/<int:id_parceiro>')
api.add_resource(ParceiroResource, '/parceiros')
api.add_resource(FaturamentoTotalResource, '/faturamento/<int:id_parceiro>')
api.add_resource(FaturamentoParceiroResource, '/faturamentos/<int:parceiro_id>')
api.add_resource(PessoaResource, '/pessoas')
api.add_resource(PessoaByIdResource, '/pessoas/<int:id_pessoa>')



api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout/<key>')

api.add_resource(EsqueciSenha, '/esquecisenha')
api.add_resource(AtualizarSenhaResource, '/esquecisenha/<string:email>')

api.add_resource(ProfissionalResource, '/profissional')
api.add_resource(ProfissionalUpdate, '/profissional/<int:id_profissional>')
api.add_resource(ProfissionalResourceById, '/profissional/<int:parceiro_id>')

api.add_resource(AgendamentoResource, "/agendamentos")
api.add_resource(AgendamentosParceiroResource, "/agendamentos/<int:parceiro_id>")
api.add_resource(AgendamentosByIdResource, "/agendamentos/<int:id_agendamento>")
api.add_resource(AgendamentosPessoaResource, "/agendamentos/pessoa/<int:pessoa_id>")

api.add_resource(ServicoResource, '/servicos')
api.add_resource(ServicoResourceById, '/servicos/<int:parceiro_id>')
api.add_resource(ServicoUpdateById, '/servicos/<int:id_servico>')
api.add_resource(ClienteResource, '/clientes')

api.add_resource(CategoriaResource, '/categorias')

api.add_resource(FaturamentoResource, '/faturamentos')


api.add_resource(AdministradorResource, '/administrador')
api.add_resource(SolicParceriaResource, '/solicitarparceria')
api.add_resource(StatusAprovacao, '/solicitarparceria/<int:id_solicitacao>/<email>')
api.add_resource(StatusAprovado, '/solicitarparceria/<email>')

api.add_resource(StatusAtivo, '/parceiros/<int:id_parceiro>')


if __name__ == '__main__':
    app.run(debug=False)
