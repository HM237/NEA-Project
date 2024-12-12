from flask import Flask
from blueprints import testing_bp

def app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.register_blueprint(testing_bp)

    return app


if __name__ == "__main__":
    app.debug = True
    app().run()

#netstat -ano | findstr :5000
#taskkill /PID 2660 /F
