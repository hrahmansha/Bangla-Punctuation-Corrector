from flask import Flask, render_template,request, jsonify, json
import logging
import play_with_model, models, data, main, postprocess
import numpy as np
import re

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/punctuation',methods=['POST'])
def punctuate():
    text = request.form.get('input_text',0,type=str)
    is_process = request.form.get('post_process',0,type=str)
    print("is process:", is_process)
    print("text: " , text)

    punctuated_data = punctuate(text)
    print(punctuated_data)
    if(is_process=="1"):
        punctuated_data = postprocess.postProcess3(punctuated_data, 0, 3, 0, 0)
    return jsonify(punctuated_data)

def punctuate(text_data):

    model_file = "Model_models.py_h256_lr0.02.pcl"
    vocab_len = len(data.read_vocabulary(data.WORD_VOCAB_FILE))
    x_len = vocab_len if vocab_len < data.MAX_WORD_VOCABULARY_SIZE else data.MAX_WORD_VOCABULARY_SIZE + data.MIN_WORD_COUNT_IN_VOCAB
    x = np.ones((x_len, main.MINIBATCH_SIZE)).astype(int)

    print("Loading model parameters...")
    net, _ = models.load(model_file, x)

    print("Building model...")
        
    word_vocabulary = net.x_vocabulary
    punctuation_vocabulary = net.y_vocabulary
    reverse_punctuation_vocabulary = {v:k for k,v in net.y_vocabulary.items()}

    text = re.sub('[,?!।]', '', text_data)
    # text = text_data
    punctuated = play_with_model.punctuate(word_vocabulary, punctuation_vocabulary, reverse_punctuation_vocabulary, text, net)

    return punctuated

if __name__ == "__main__":
    app.run(debug=True)