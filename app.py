from flask import Flask,send_from_directory
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from models import *
from book import book 
from member import member
from user import user_bp

# app initializ
app = Flask(__name__)
migrate = Migrate()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbase.db"

# initialize database and migration
db.init_app(app)
migrate.init_app(app,db)

## app blueprint
app.register_blueprint(book,url_prefix="/books")
app.register_blueprint(member,url_prefix="/members")
app.register_blueprint(user_bp,url_prefix="/user")


# Swagger UI setup
SWAGGER_URL = "/swagger"
API_URL = "/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,  # Swagger JSON file
    config={"app_name": "Library API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve swagger.json file
@app.route("/swagger.json")
def swagger_json():
    return send_from_directory(".", "swagger.json")

# run server
if __name__ == "__main__":
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(debug=True)

