from flask import Blueprint, request, jsonify
import json
import os

# 1. Skapa Blueprinten för bilar
car_bp = Blueprint('car_bp', __name__)

DATA_FILE = 'cars.json'

# --- HJÄLPFUNKTIONER FÖR FILHANTERING ---

def read_data():
    """Läser in data från cars.json. Returnerar en tom lista om filen inte finns."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_data(data):
    """Skriver data till cars.json."""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# --- API ENDPOINTS (CRUD) ---

# 1. READ (Hämta alla bilar)
# ÄNDRING: Här använder vi @car_bp istället för @app
@car_bp.route('/cars', methods=['GET'])
def get_all_cars():
    """Returnerar alla bilar i registret."""
    cars = read_data()
    return jsonify(cars), 200

# 2. READ (Hämta specifik bil via registreringsnummer)
@car_bp.route('/cars/<reg_nr>', methods=['GET'])
def get_car(reg_nr):
    """Returnerar en specifik bil baserat på registreringsnummer."""
    cars = read_data()
    car = next((c for c in cars if c['reg_nr'].upper() == reg_nr.upper()), None)
    
    if car:
        return jsonify(car), 200
    else:
        return jsonify({"error": "Bilen hittades inte"}), 404

# 3. CREATE (Lägg till en ny bil)
@car_bp.route('/cars', methods=['POST'])
def add_car():
    """Lägger till en ny bil. Kräver att reg_nr finns med i JSON-datan."""
    new_car = request.get_json()
    cars = read_data()
    
    if not new_car or 'reg_nr' not in new_car:
        return jsonify({"error": "Registreringsnummer (reg_nr) saknas i datan"}), 400
        
    for car in cars:
        if car['reg_nr'].upper() == new_car['reg_nr'].upper():
            return jsonify({"error": "En bil med detta registreringsnummer finns redan"}), 409
            
    new_car['reg_nr'] = new_car['reg_nr'].upper()
    cars.append(new_car)
    write_data(cars)
    
    return jsonify({"message": "Bilen har lagts till", "car": new_car}), 201

# 4. UPDATE (Uppdatera befintlig bil)
@car_bp.route('/cars/<reg_nr>', methods=['PUT'])
def update_car(reg_nr):
    """Uppdaterar information för en bil via registreringsnumret."""
    updated_data = request.get_json()
    cars = read_data()
    
    for car in cars:
        if car['reg_nr'].upper() == reg_nr.upper():
            for key, value in updated_data.items():
                if key != 'reg_nr':
                    car[key] = value
            
            write_data(cars)
            return jsonify({"message": f"Bilen med reg_nr {reg_nr.upper()} har uppdaterats", "car": car}), 200
            
    return jsonify({"error": "Bilen hittades inte"}), 404

# 5. DELETE (Ta bort bil)
@car_bp.route('/cars/<reg_nr>', methods=['DELETE'])
def delete_car(reg_nr):
    """Tar bort en bil från registret via registreringsnummer."""
    cars = read_data()
    
    new_cars_list = [c for c in cars if c['reg_nr'].upper() != reg_nr.upper()]
    
    if len(cars) == len(new_cars_list):
        return jsonify({"error": "Bilen hittades inte"}), 404
        
    write_data(new_cars_list)
    return jsonify({"message": f"Bilen med reg_nr {reg_nr.upper()} har raderats"}), 200