def create_app(full = True):
    from flask import Flask
    import sys
    sys.path.append('jaws')

    app = Flask(__name__)
    app.static_path = app.static_folder

    _setup_config(app)

    if full:
        from randblock.view.jinja_helpers import setup_jinja_helpers
        setup_jinja_helpers(app)

    _setup_blueprints(app)

    return app


def get_environment():
    import os
    """return the environment from an environment variable,
    should be development|test|staging|production"""
    return os.environ.get('ENVIRONMENT', 'development')


def _setup_config(app):
    from randblock.config import config
    app.config.update(config)


def _setup_blueprints(app):
    from randblock.view.blueprints.main import main
    
    app.register_blueprint(main)

