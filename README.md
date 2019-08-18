# Disaster Responses Analysis

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# Disaster Responses

In this project, there are two datesets: disaster categories and disaster messages which contains 36 response categories and data we build models using  NLP and Machine learning pipelines and build an web application with the optimized classifier to predict in which response category the message belongs.

## Model Pipeline Usage
Two parts of this project:
   1. The ETL pipeline in the '/data' directory:
        1.1 Combine the two given csv datasets(categories and messages)
        1.2 Cleanse the data and convert categories to numeric
        1.3 Store dataset into SQLite database
        
   2. The NLP and ML pipeline in the '/models' directory
        2.1 Split the dataset into training and testing datasets which contain comments and labels
        2.2 Build a text processing and ML pipeline
        2.3 Train a model using sklearn GridSearchCV
        2.4 Use test dataset to predict responses and output results
        2.5 Save the model as .pkl file
        
## Installation
 ##### Load dataset and build model
- To run ETL pipeline that cleans data and stores in database
        `$ python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
- To run ML pipeline that trains classifier and saves
        `$ python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`
 ##### The Flask app in the './app' directory
- Run the following command in the app's directory to run your web app.
    `$ python run.py`
- Go to http://0.0.0.0:3001/

## Requirement
- pandas==0.23.0
- numpy==1.15.4
- json==2.0.9
- sklearn==0.20.2
- nltk==3.2.4
- matplotlib==2.2.2
- seaborn==0.9.0
## License
non license
