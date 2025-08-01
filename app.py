from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/articles.json')
def get_articles():
    with open('articles.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
