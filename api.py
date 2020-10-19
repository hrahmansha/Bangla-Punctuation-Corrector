from flask import Flask, render_template,request, jsonify, json
import logging


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/punctuation',methods=['POST'])
def punctuate():
    text = request.form.get('input_text',0,type=str)
    print("text: " , text)
    return jsonify(text)

if __name__ == "__main__":
    app.run(debug=True)