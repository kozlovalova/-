from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

JSON_FILE = "tours.json"

# Чтение данных из JSON-файла
def read_json():
    try:
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w") as file:
                json.dump({"tours": [], "bookings": []}, file)
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise Exception("Ошибка чтения JSON-файла. Проверьте его структуру.")

# Запись данных в JSON-файл
def write_json(data):
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise Exception(f"Ошибка записи в JSON-файл: {str(e)}")

# GET-эндпоинт для получения списка туров
@app.route("/tours", methods=["GET"])
def get_tours():
    try:
        data = read_json()
        return jsonify(data["tours"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST-эндпоинт для добавления нового бронирования
@app.route("/book", methods=["POST"])
def book_tour():
    try:
        data = read_json()
        booking = request.json

        # Валидация обязательных полей
        required_fields = ["tour_id", "name", "seats"]
        for field in required_fields:
            if field not in booking:
                return jsonify({"error": f"Поле '{field}' является обязательным."}), 400

        # Проверка формата данных
        if not isinstance(booking["tour_id"], int) or booking["tour_id"] <= 0:
            return jsonify({"error": "Поле 'tour_id' должно быть положительным числом."}), 400
        if not isinstance(booking["name"], str) or not booking["name"].strip():
            return jsonify({"error": "Поле 'name' должно быть непустой строкой."}), 400
        if not isinstance(booking["seats"], int) or booking["seats"] <= 0:
            return jsonify({"error": "Поле 'seats' должно быть положительным числом."}), 400

        # Проверяем, существует ли тур и достаточно ли мест
        tour = next((t for t in data["tours"] if t["id"] == booking["tour_id"]), None)
        if not tour:
            return jsonify({"error": "Тур не найден."}), 404

        if tour["available_seats"] < booking["seats"]:
            return jsonify({"error": "Недостаточно мест для бронирования."}), 400

        # Обновляем данные о турах и добавляем бронирование
        tour["available_seats"] -= booking["seats"]
        new_booking = {
            "id": len(data["bookings"]) + 1,
            "tour_id": booking["tour_id"],
            "name": booking["name"].strip(),
            "seats": booking["seats"]
        }
        data["bookings"].append(new_booking)
        write_json(data)

        return jsonify(new_booking), 201

    except json.JSONDecodeError:
        return jsonify({"error": "Ошибка в JSON-данных. Проверьте запрос или структуру файла."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET-эндпоинт для получения списка бронирований
@app.route("/bookings", methods=["GET"])
def get_bookings():
    try:
        data = read_json()
        return jsonify(data["bookings"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "main":
    app.run(debug=True)