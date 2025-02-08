from flask import Flask
from routes.auth import auth_bp
from routes.tracks import tracks_bp

app = Flask(__name__)
app.secret_key = "random_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(tracks_bp)


if __name__ == '__main__':
    app.run(debug=True)