from .extension import db, bcrypt, jwt, migrate, session


def connect_extension(app) -> None:
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.config['SESSION_SQLALCHEMY'] = db

    session.init_app(app)
