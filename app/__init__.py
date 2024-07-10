from flask import Flask
from app.database import db, migrate
from graphql_server.flask import GraphQLView
from app.schema import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

db.init_app(app)
migrate.init_app(app, db)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True
))

from app import models
