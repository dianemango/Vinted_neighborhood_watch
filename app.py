from flask import Flask
from vinted_tracker import run_tracker

app = Flask(__name__)

@app.route('/')
def index():
    return "Vinted Tracker API en ligne 🚀"

@app.route('/run', methods=['GET'])
def run():
    run_tracker()
    return "✅ Veille Vinted exécutée avec succès !"

if __name__ == "__main__":
    app.run()
