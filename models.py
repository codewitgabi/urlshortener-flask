from flask_sqlalchemy import SQLAlchemy

# database instance
db = SQLAlchemy()


class Url(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    old_url = db.Column(db.String, unique=True, nullable=False)
    new_url = db.Column(db.String, primary_key=True, unique=True, nullable=False)

    def __str__(self):
        return self.new_url


