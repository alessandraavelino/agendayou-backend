from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db, migrate

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
from resources.suporte import SuporteResource, SuporteResourceById

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://alessandra:jh1mhvCb2Gq3Q20jacHf5E9lPVNYgqTl@dpg-ciev2t15rnujc4pnee2g-a.oregon-postgres.render.com/agendayou"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

api = Api(app)

# Parceiro
api.add_resource(DeletarParceiro, '/parceiros/<int:id_parceiro>')
api.add_resource(ParceiroResource, '/parceiros')
api.add_resource(StatusAtivo, '/parceiros/<int:id_parceiro>')

# Faturamento
api.add_resource(FaturamentoTotalResource, '/faturamento/<int:id_parceiro>')
api.add_resource(FaturamentoParceiroResource, '/faturamentos/<int:parceiro_id>')
api.add_resource(FaturamentoResource, '/faturamentos')

# Pessoa
api.add_resource(PessoaResource, '/pessoas')
api.add_resource(PessoaByIdResource, '/pessoas/<int:id_pessoa>')

# Login
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout/<key>')

# Esqueci Senha
api.add_resource(EsqueciSenha, '/esquecisenha')
api.add_resource(AtualizarSenhaResource, '/esquecisenha/<string:email>')

# Profissional
api.add_resource(ProfissionalResource, '/profissional')
api.add_resource(ProfissionalUpdate, '/profissional/<int:id_profissional>')
api.add_resource(ProfissionalResourceById, '/profissional/<int:parceiro_id>')

# Agendamentos
api.add_resource(AgendamentoResource, "/agendamentos")
api.add_resource(AgendamentosParceiroResource, "/agendamentos/<int:parceiro_id>")
api.add_resource(AgendamentosByIdResource, "/agendamentos/<int:id_agendamento>")
api.add_resource(AgendamentosPessoaResource, "/agendamentos/pessoa/<int:pessoa_id>")

# Serviços
api.add_resource(ServicoResource, '/servicos')
api.add_resource(ServicoResourceById, '/servicos/<int:parceiro_id>')
api.add_resource(ServicoUpdateById, '/servicos/<int:id_servico>')

# Clientes
api.add_resource(ClienteResource, '/clientes')

# Categorias
api.add_resource(CategoriaResource, '/categorias')

# Administrador
api.add_resource(AdministradorResource, '/administrador')

# Solicitar parceria
api.add_resource(SolicParceriaResource, '/solicitarparceria')
api.add_resource(StatusAprovacao, '/solicitarparceria/<int:id_solicitacao>/<email>')
api.add_resource(StatusAprovado, '/solicitarparceria/<email>')

# Suporte
api.add_resource(SuporteResource, '/suporte')
api.add_resource(SuporteResourceById, '/suporte/<id_suporte>')

if __name__ == '__main__':
    app.run(debug=False)
