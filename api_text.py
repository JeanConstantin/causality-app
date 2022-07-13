from flask import Flask, request, render_template
import pickle, spacy
from argument_splitting_func import *
from causal_model import *
import torch
from transformers.models.camembert.modeling_camembert import CamembertForSequenceClassification
from transformers import CamembertTokenizer
from transformers import TextClassificationPipeline

nlp = spacy.load('fr_core_news_sm', disable=['ner', 'lemmatizer',  'attribute_ruler'])

with open('connective_patterns_french.pkl', 'rb') as f:
    connective_patterns = pickle.load(f)

model = CamembertForSequenceClassification.from_pretrained("jeanconstantin/causal_bert_fr", id2label={0: 'not causal', 1: 'reason', 2: 'result'})
tokenizer = CamembertTokenizer.from_pretrained("camembert/camembert-base")
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def split_sent():
    text = request.form['text']
    processed_text = split_argument(text, ['…', '.', ';', ','], connective_patterns, nlp)
    causal_args = find_causal(processed_text, pipe, sensitivity=0.8)
    reason_indices = causal_args['reason']
    result_indices = causal_args['result']
    
    return render_template('home.html', output_text = processed_text, reason_indices=reason_indices, result_indices=result_indices)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


#https://stackoverflow.com/questions/68630368/how-to-highlight-text-in-flask
