from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db, migrate
from model.endereco import Endereco
from model.pessoa import Pessoa
from model.parceiro import Parceiro
from model.usuario import Usuario
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
pessoa = Pessoa("Alê", "23/01/2002", "123.456.789-80", "83996097405", endereco)
print(pessoa)

parceiro = Parceiro("Maria", "10/01/2001", "987.654.321-20", "40028922", endereco, "Mary Beautiful", "Beleza", "Aprovado")
print(parceiro)

usuario = Usuario("alessandra@gmail.com", "senhaultrasecreta")
print(usuario)

# Resources

if __name__ == '__main__':
    app.run(debug=False)