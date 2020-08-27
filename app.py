import logging
logging.basicConfig(format='%(asctime)s [%(filename)-24.24s] %(levelname)s %(lineno)d: %(message)s', 
                    level=logging.INFO,
                    datefmt='%I:%M:%S')
import flask
from flask import Flask, request, render_template
import json
import use_model
import bm25_model
import sentenceBERT_model
import sentenceROBERTA_model
import infersent_model
import bert_model

from datetime import timedelta
import time


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_predictions', methods=['post'])
def get_prediction():
    corpus = []
    d = {}
    try:
        input_query = request.json['input_query']
        input_corpus = request.json['input_corpus']
        split_token = request.json['split_token']
        top_k = request.json['top_k']
        if split_token == '0':
            corpus = input_corpus.split('\n')
        elif split_token == '1':
            corpus = input_corpus.replace('\n', '').split('.')
                
        models = [{
                    'name': 'use',
                    'obj': use_model,
                    'desc': 'Universal Sentence Encoder'
                },{
                    'name': 'bm25',
                    'obj': bm25_model,
                    'desc': 'BM25'
                },{
                    'name': 'sentenceBERT',
                    'obj': sentenceBERT_model,
                    'desc': 'Sentence Transformers BERT'
                },{
                    'name': 'infersent',
                    'obj': infersent_model,
                    'desc': 'Infersent Glove'
                },{
                    'name': 'bert',
                    'obj': bert_model,
                    'desc': 'BERT mean pooling'
                },{
                    'name': 'roberta',
                    'obj': sentenceROBERTA_model,
                    'desc': 'Sentence Transformers RoBERTA'
                }
            ]
        for model in models:
            model_name = model['name']
            t0 = time.time()        
            scores, sentences = model['obj'].get_scores(input_query, corpus, int(top_k))        
            time_taken = str(timedelta(seconds=time.time() - t0))
            d[f'{model_name}_scores'] = list(scores)
            d[f'{model_name}_sentences'] = sentences
            d[f'{model_name}_elapsed'] = time_taken    
        
        d['meta_info'] = [{'name': model['name'], 'desc': model['desc'] } for model in models]

        return app.response_class(response=json.dumps(d), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


if __name__ == '__main__':
    print("starting server")
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)
