from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db, migrate
from model.endereco import Endereco
from model.pessoa import Pessoa
from model.parceiro import Parceiro
from model.login import Login

from resources.parceiro import ParceiroResource
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
endereco = Endereco("58255000", "Paraíba", "Belém", "Centro", "Rua São Joaquim", "160")
pessoa = Pessoa("Alê", "ale@mail.com", "12343", "23/01/2002", "123.456.789-80", "83996097405", endereco)
print(pessoa)

parceiro = Parceiro("dfdsf", "rtret", "Maria", "10/01/2001", "987.654.321-20", "40028922", endereco, "Mary Beautiful", "Beleza")
print(parceiro)


# Resources
api.add_resource(ParceiroResource, '/parceiros')
if __name__ == '__main__':
    app.run(debug=False)