from flask import Flask
from flasgger import Swagger
from controllers.userController import user_bp
from controllers.roleController import role_bp
from controllers.claimController import claim_bp
from controllers.userClaimsController import userClaim_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from swagger_config import template
import pymysql
import os

load_dotenv()

#inicia a aplicação
app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
#configura o Flask atrás de um servidor Proxy (nginx)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

#configura a conexão com o banco de dados
db_uri = '{connection}://{user}:{pwd}@{host}:{port}/{db}'.format(connection=os.environ.get("DB_CONNECTION", "mysql"),
                                                                   user=os.environ.get("DB_USERNAME", "root"),
                                                                   pwd=os.environ.get("DB_PASSWORD", "root"),
                                                                   host=os.environ.get("DB_HOST", "localhost"),
                                                                   port=os.environ.get("DB_PORT", "3306"),
                                                                   db=os.environ.get("DB_DATABASE", "flask"))
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#'mysql+pymysql://root:root@database:3306/shipay'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicia o banco e cria as tabelas
from db import db
db.init_app(app)
with app.app_context():
    db.create_all()

#registra as rotas utilizando o pacote blueprint do Flask
app.register_blueprint(claim_bp, url_prefix='/claims')
app.register_blueprint(userClaim_bp, url_prefix='/user-claims')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(role_bp, url_prefix='/roles')



app.config['SWAGGER'] = {
    'title': 'Teste Shipay API',
    'uiversion': 3
}

#inicia o swagger para a documentação da API
swagger = Swagger(app, template=template)


if __name__ == '__main__':
    # from db import db
    # db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    app.run(debug=os.environ.get("DEBUG"))