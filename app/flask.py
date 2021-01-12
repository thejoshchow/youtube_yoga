from flask import Flask, render_template, request, jsonify
import pandas as pd

from model_data.predict import predict

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    style = user_data['style']
    vid_list = _recommend_vid(style)
    return jsonify({'result': vid_list})

def _recommend_vid(style):
    user_data = request.json
    style = user_data['style']
    data = predict(style)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)