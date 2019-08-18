#prepare dataset from csv file

import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    #load messages and categories dataset and then merge them into on dataframe by column”id”
    
    #load messages dataset from csv file
    messages_dataset = pd.read_csv(messages_filepath)
    
    #load categories dataset from csv file
    categories_dataset = pd.read_csv(categories_filepath)
    
    #merge these datasets and return data frame
    return pd.merge(messages_dataset, categories_dataset, on='id')


def clean_data(df):
    
    # get the value of “categories“ column and split it by ‘;’ and create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(pat=';', n=None, expand=True)

    # use the first row to extract a list of new column names for categories.
    category_colnames = categories.iloc[0].str[:-2]

    # rename the columns of `categories` data frame
    categories.columns = category_colnames

    for column in categories:
        # get the last character of the string value of each category column in categories data frame
        # and cast it to int
        categories[column] = categories[column].str[-1].astype(int)

    # drop the original categories column from `df`
    df = df.drop(columns='categories')

    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1)

    # drop duplicates
    df = df.drop_duplicates(keep='first')

    return df


def save_data(df, database_filename):
    #Writes a dataframe to a Sql-lite Database
    print('Writing {} to {} database: '.format(df, database_filename))
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('DisasterResponse', engine, index=False)
    #df.to_sql(database_filename[0:-3], engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '
              'datasets as the first and second argument respectively, as '
              'well as the filepath of the database to save the cleaned data '
              'to as the third argument. \n\nExample: python process_data.py '
              'disaster_messages.csv disaster_categories.csv '
              'DisasterResponse.db')


if __name__ == '__main__':
    main()