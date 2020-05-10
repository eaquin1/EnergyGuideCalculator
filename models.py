from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Appliance(db.Model):
    """Appliances Wattage Model"""
    __tablename__ = "appliances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    watts = db.Column(db.Integer)
    category = db.Column(db.Text)

    def __repr__(self):
        """Show info about appliance"""
        a = self
        return f"<Appliance {a.id} {a.name} {a.watts} {a.category}>"