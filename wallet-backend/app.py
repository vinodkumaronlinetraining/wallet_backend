from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Wallet app API is running"})

@app.route("/api/test")
def test():
    return jsonify({
        "status": "ok",
        "version": "1.0",
        "message": "Backend connected"
    })

if __name__ == "__main__":
    app.run(debug=True)