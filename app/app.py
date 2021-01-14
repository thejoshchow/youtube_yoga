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
    yoga = user_data['yoga']
    result_table = _recommend_vid(yoga)
    return result_table

def _recommend_vid(yoga):
    headings = ['Link', 'Title']
    model = predict(yoga)
    # data = model.vid_embed()
    data = model.vid_table()
    data = data.values.tolist()
    return render_template('recommend.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 