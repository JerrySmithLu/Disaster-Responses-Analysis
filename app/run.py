import json
import plotly
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
from sklearn.externals import joblib
from sqlalchemy import create_engine
import seaborn as sns

#nltk.download('punkt')
app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', engine)
#engine = create_engine('sqlite:///Messages_Categories.db')
#df = pd.read_sql_table('Messages_Categories', engine)

# load model
model = joblib.load("../models/classifier.pkl")

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)      
    
    #count the number of comments under each label
    categories_name = list(df.columns.values)
    del categories_name[0]
    del categories_name[0]
    del categories_name[0]
    categories_counts = df.iloc[:,2:].sum().values
    
    #Counting the number of comments having multiple labels.
    rowSums = df.iloc[:,2:].sum(axis=1)
    multilabel_counts = rowSums.value_counts()
    multilabel_counts = multilabel_counts.iloc[1:]

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        }
    ]
    categories = [
        {
            'data': [
                Bar(
                    x=categories_name,
                    y=categories_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Categories',
                'yaxis': {
                    'title': "Number of comments"
                },
                'xaxis': {
                    'title': "Comment Type"
                }
            }
        }
    ]
    
    multi_categories = [
        {
            'data': [
                Bar(
                    x=multilabel_counts.index,
                    y=multilabel_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Multiple Categories',
                'yaxis': {
                    'title': "Number of comments"
                },
                'xaxis': {
                    'title': "Number of labels"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    category_ids = ["category-{}".format(i) for i, _ in enumerate(categories)]
    category_graphJSON = json.dumps(categories, cls=plotly.utils.PlotlyJSONEncoder)
    
    multilcategory_ids = ["multicategories-{}".format(i) for i, _ in enumerate(multi_categories)]
    multilcategory_graphJSON = json.dumps(multi_categories, cls=plotly.utils.PlotlyJSONEncoder)
    print(multilcategory_ids)
    # render web page with plotly graphs    
    
    return render_template('master.html', ids=ids, graphJSON=graphJSON, category_ids=category_ids, category_graphJSON = category_graphJSON, multilcategory_ids=multilcategory_ids,multilcategory_graphJSON=multilcategory_graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()