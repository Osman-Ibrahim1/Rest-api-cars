from flask import Flask
from routes import car_bp  # Importera din Blueprint från routes.py

app = Flask(__name__)

# Registrera din Blueprint i appen
app.register_blueprint(car_bp)

if __name__ == '__main__':
    app.run(debug=True)