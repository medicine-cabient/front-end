import spacy
import pandas as pd
import numpy as np
import sklearn
import pickle
from joblib import load
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.tokenizer import Tokenizer
import re
import spacy.cli
from collections import OrderedDict



# import statements
# import numpy
# from sklearn.neighbors import nearestneighbors
#
#
# df = pd.read_csv("our.csv")


# drews wrangling 


# s = standardscaler()
# X = s.fit_transform(df)
# nn = nearestneighbors(5)
# nn.fit(X)
# 
# python -m spacy download en_core_web_lg
spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")
# tokenizer
tokenizer = Tokenizer(nlp.vocab)


# df = pd.read_csv('cannabis.csv')

# #  SPAIN IS REGISTERING AS PAIN!!! MAKE A DROP WORD 
# STOP_WORDS = nlp.Defaults.stop_words.union([' ', 'spain', 'los', 'sap', 'mother', 
#                                             'petite', 'tonic', 'so', 'ash', 
#                                             'rain', 'in', 'app', 'hyper', 
#                                             'tension', '\xa0 ', ' ', '\xa0'])


# def get_lemmas(text):
#   """Returns `lemmas` in a list"""
#   tokens = []
#   doc = nlp(text)

#   for token in doc:
#     if (token.is_stop == False) & (token.is_punct == False) & (token.pos_!= 'PRON') & (token.text.lower() not in STOP_WORDS):
#       tokens.append(token.lemma_)

#   return tokens

# def remove_data(text):

# #     # remove non-alphanumeric
#     nonalpha = re.sub(r"\b[a-zA-Z]\b", "", text)
#     #nonalpha = re.sub('[^1-9]', ' ', text)
#     # make all text lowercase
    
#     return nonalpha

# def wrangle(df):
#   df = df.copy()
  
#   #  Only rows with values greater than 2.0 stay
#   # df = df[df['Rating'] > 2.0]

#   df = df.fillna("")

#   # concatenating strings of text using `cat`
#   df['FullText'] = df['Description'].str.cat(df['Type'], sep=" ")
#   df['FullText'] = df['FullText'].str.cat(df['Effects'], sep=" ")
#   df['FullText'] = df['FullText'].str.cat(df['Flavor'], sep=" ")

#   #  This line combines the entire row into a string exluding floats and integers call df['text']
#   df['FullText'] = df['FullText'].str.cat(df['Description'], sep=" ")

#   # Renaming columns
#   df.columns = ['Name', 'Type', 'Rating', 'Effects', 'Flavor', 'Description', 'FullText']

  

#   df['cleaned_name'] = df['Name'].apply(lambda x: "".join(x))
#   df['cleaned_name'] = df['cleaned_name'].apply(lambda x: x.replace("-"," "))
#   df['cleaned_name'] = df['cleaned_name'].apply(lambda x: x.lower())


#   #List of dupicate columns BELOW - Don't Reference this because 
#   #column names changed later on
#   #['Name', 'Type', 'Rating', 'Effects', 'Flavor', 
#   #'Description', 'FullText', 'lemmas', 'cleaned_name', 'count_text']

#   cols = ["cleaned_name", "Rating", "Type", "Effects", 
#                "Flavor", "Description", "FullText"]
#   df = df[cols]
  

#   ls_need_lemmas = ['Type', 'Effects', 'Flavor', 'FullText']

  
#   for val in ls_need_lemmas:
#     df[val] = df[val].apply(get_lemmas)
#     df[val] = df[val].map(lambda x: list(set(map(str.lower, x))))
#     # df[val] = df[val].apply(lambda x: re.sub('[^a-zA-Z 0-9]', ' ',x))
#     df[val] = df[val].str.join(", ")


#   #  Rename columns
#   df.columns = ['Strain', 
#                 'Rating',
#                 'Type', 
#                 'Effects', 
#                 'Flavor', 
#                 'Description', 
#                 'FullText']

#   df['tokens'] = df['FullText'].apply(get_lemmas)

  
#   condition = [df['Rating'].between(4.5, 5.0), 
#                df['Rating'].between(3.2, 4.5),
#                df['Rating'].between(0, 3.2)]
#   value_rating_basket = ['Great', 'Good', 'Bad']
#   df['Rating Category'] = np.select(condition, value_rating_basket, 0)


#   ls_dosage = ['dose', 'dosage', 'potency', 'potent']
    
#   df['Dosage_in_Descrip'] = df['FullText'].str.findall(f"({'|'.join(ls_dosage)})").str.join(', ').replace('', np.NaN)
#   df['Dosage_in_Descrip'].fillna('none', inplace=True)


#   #  Pulls out words that describe `Ailments` from `FullText` column

#   values_issues = {'sore', 'migraine', 'rash', 'allergy', 
#                    'inflammation', 'pain', 'seizure','catatonic'
#                    'spasm', 'appetite', 'weight', 'cramp'
#                    'cold', 'influenza', 'glaucoma', 'arthritis', 'sclerosis',
#                    'stress', 'ache', 'insomnia', 'sad', 
#                    'cancer', 'anxiety', 'foggy',
#                    'epilepsy', 'nausea', 'depression', 'sleep', 
#                    'chemotherapy', 'soreness'
#                    'add', 'adhd', 'ocd', 'hypertension', 'indigestion'}

#   #  Flags `Issues` values(ABOVE)
#   df['Flagged Ailments'] = df['FullText'].apply(lambda x: sum(i in values_issues for i in x.split(", ")))

  

#   ls_values_issues = ['sore', 'migraine', 'rash', 'allergy', 
#                 'inflammation', 'pain', 'seizure', 'catatonic' 
#                 'spasm', 'appetite', 'weight', 'cramp'
#                 'cold', 'influenza', 'glaucoma', 'arthritis', 'sclerosis',
#                 'stress', 'ache', 'insomnia', 'sad', 
#                 'cancer', 'anxiety', 'foggy',
#                 'epilepsy', 'nausea', 'depression', 'sleep', 
#                 'chemotherapy', 'soreness' 
#                 'add', 'adhd', 'ocd', 'hypertension', 'indigestion']

#   df['Ailments'] = (df['FullText'].str.findall(f"({'|'.join(ls_values_issues)})").str.join(', ').replace('', np.NaN))
#   df['Ailments'] = df['Ailments'].fillna(0)

 
#   df['count_ailments'] = df['Ailments'].str.count(',').add(1)
#   df['count_ailments'] = df['count_ailments'].fillna(0)

#   #  this counted the text in `FullText` - Ended up not using this
#   df['count_text'] = df['FullText'].apply(lambda x: len(x)) 
#   df['Strain'] = df['Strain'].apply(lambda x: x.title())
#   df['Type'] = df['Type'].apply(lambda x: x.title())
#   df['Effects'] = df['Effects'].apply(lambda x: x.title())
#   df['Flavor'] = df['Flavor'].apply(lambda x: x.title())
#   df = remove_data(df['FullText'])  
#   return df

# test_df = wrangle(df)
# # Create Pipeline Components
# # Tunning Parameters
# # Instantiate vectorizer object
# data = test_df['FullText']
# tfidf = TfidfVectorizer(stop_words='english', 
#                         ngram_range=(1,2),
#                         max_df=.95,
#                         min_df=5,
#                         tokenizer=get_lemmas)
# # Create a vocabulary and get word counts per document
# dtm = tfidf.fit_transform(data) # Similiar to fit_predict
# Print word counts
# Get feature names to use as dataframe column headers
# dtm = pd.DataFrame(dtm.todense(), columns=tfidf.get_feature_names())
# View Feature Matrix as DataFrame

# nn = NearestNeighbors(n_neighbors=5, algorithm='kd_tree', radius=.5)
# nn.fit(dtm)
# review = []

# new = tfidf.transform(review)
# preds = nn.kneighbors(new.todense())

# # saving the model
# filename = "mvp.product"
# pickle.dump(nn, open(filename, "wb"))

# #  Loading the model
# model = pickle.load(open("mvp.product", "rb"))
# review = ["catatonic"]
# tran = tfidf.transform(review)
# model.kneighbors(tran.todense())[1]

test_df = pd.read_csv("test_df.csv")

def pred_function(x):
    """Make prediction and return nested dictionary
    
       x = string
    """
    # Load mode file and perform prediction
    model = load("mvp_product.joblib")
    tfidf = pickle.load(open("vectorizer.pickle", "rb"))
    global review
    review = [x]
    trans = tfidf.transform(review)
    global pred
    pred = model.kneighbors(trans.todense())[1][0]
    
    


    #create empty dictionary
    pred_dict = {}
    
    #summary statistics of 5 closest neighbors
    for x in pred:
        print("\n                 --DISCLAIMER! Dosage Size recommendations will vary between users.--")
        print("\nStrain: ", test_df["Strain"][x])
        print("Dosage Size: ", test_df["Dosage Size"][x])
        print("\nRating Category: ", test_df["Rating Category"][x])
        print("Rating: ", test_df["Rating"][x])
        print("\nType: ", test_df["Type"][x])
        print("\nDescription: ", test_df["Description"][x])
        print("\nFlavor: ", test_df["Flavor"][x])
        print("\nEffects: ", test_df["Effects"][x])
        print("\nAilments: ", test_df["Ailments"][x])
        print("\n____________________________________")

                # add new dictionary to pred_dict containing predictions
        preds_dict = OrderedDict({(1+len(pred_dict)) : {"strain": test_df["Strain"][x],
                                          "dosage size": test_df["Dosage Size"][x],
                                          "rating category": test_df["Rating Category"][x], 
                                          "rating": test_df["Rating"][x],
                                          "type": test_df["Type"][x],
                                          "description": test_df["Description"][x],
                                          "flavor": test_df["Flavor"][x],
                                          "effects": test_df["Effects"][x],
                                          "ailments": test_df["Ailments"][x]}})
        pred_dict.update(preds_dict)
    
    return pred_dict

    # for x in pred:
    #     top_5_recommendations = ["\n                 --DISCLAIMER! Dosage Size recommendations will vary between users.--",
    #         "\nStrain: ", test_df["Strain"][x],
    #         "Dosage Size: ", test_df["Dosage Size"][x],
    #         "\nRating Category: ", test_df["Rating Category"][x],
    #         "\nRating: ", test_df["Rating"][x],
    #         "\nType: ", test_df["Type"][x],
    #         "\nDescription: ", test_df["Description"][x],
    #         "\nFlavor: ", test_df["Flavor"][x],
    #         "\nEffects: ", test_df["Effects"][x],
    #         "\nAilments: ", test_df["Ailments"][x],
    #         "\n____________________________________"]

    #             # add new dictionary to pred_dict containing predictions
    #     preds_dict = {"strain": test_df["Strain"][x],
    #                 "dosage size": test_df["Dosage Size"][x],
    #                      "rating category": test_df["Rating Category"][x], 
    #                                       "rating": test_df["Rating"][x],
    #                                       "type": test_df["Type"][x],
    #                                       "description": test_df["Description"][x],
    #                                       "flavor": test_df["Flavor"][x],
    #                                       "effects": test_df["Effects"][x],
    #                                       "ailments": test_df["Ailments"][x]}
    #     pred_dict.update(preds_dict)
    
    # return pred_dict

# def print_out(pred):
#     pred_dict = {}
    
#     #summary statistics of 5 closest neighbors
#     for x in pred[:5]:
#         return ("\n                 --DISCLAIMER! Dosage Size recommendations will vary between users.--",
#         "\nStrain: ", test_df["Strain"][x],
#         "Dosage Size: ", test_df["Dosage Size"][x],
#         "\nRating Category: ", test_df["Rating Category"][x],
#         "\nRating: ", test_df["Rating"][x],
#         "\nType: ", test_df["Type"][x],
#         "\nDescription: ", test_df["Description"][x],
#         "\nFlavor: ", test_df["Flavor"][x],
#         "\nEffects: ", test_df["Effects"][x],
#         "\nAilments: ", test_df["Ailments"][x],
#         "\n____________________________________")

    #             # add new dictionary to pred_dict containing predictions
    #     preds_dict = OrderedDict({(1+len(pred_dict)): {"strain": test_df["Strain"][x],
    #                                       "dosage size": test_df["Dosage Size"][x],
    #                                       "rating category": test_df["Rating Category"][x], 
    #                                       "rating": test_df["Rating"][x],
    #                                       "type": test_df["Type"][x],
    #                                       "description": test_df["Description"][x],
    #                                       "flavor": test_df["Flavor"][x],
    #                                       "effects": test_df["Effects"][x],
    #                                       "ailments": test_df["Ailments"][x]}})
    #     pred_dict.update(preds_dict)

    # return pred_dict