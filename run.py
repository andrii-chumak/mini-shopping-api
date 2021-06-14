from app import create_app
from database import db

app = create_app()
db.init_app(app)
