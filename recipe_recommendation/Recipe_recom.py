import sys
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from ingredient_parser import ingredient_parser
import pickle
import unidecode, ast

# Add the parent directory to the system path to import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import path_config  as PC

# Top-N recomendations order by score
def get_recommendations(N, scores):
    # load in recipe dataset 
    df_recipes = pd.read_csv(PC.PARSED_DATA_PATH)
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations 
    recommendation = pd.DataFrame(columns = ['score', 'recipe', 'ingredients', 'directions', 'url'])
    count = 0
    for i in top:
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i][0][0]))
        recommendation.at[count, 'recipe'] = title_parser(df_recipes['title'][i])
        recommendation.at[count, 'ingredients'] = ingredient_parser_final(df_recipes['ingredients'][i])
        recommendation.at[count, 'directions'] = df_recipes['directions'][i]
        recommendation.at[count, 'url'] = df_recipes['link'][i]
        # recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        # recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i][0]))
        count += 1
    return recommendation

# neaten the ingredients being outputted 
def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        ingredients = ast.literal_eval(ingredient)
    
    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients

def title_parser(title):
    title = unidecode.unidecode(title)
    return title 

def RecSys(ingredients, N=5):
    """
    The reccomendation system takes in a list of ingredients and returns a list of top 5 
    recipes based of of cosine similarity. 
    :param ingredients: a list of ingredients
    :param N: the number of reccomendations returned 
    :return: top 5 reccomendations for cooking recipes
    """

    # load in tdidf model and encodings 
    with open(PC.TFIDF_ENCODINGS_PATH, 'rb') as f:
        tfidf_encodings = pickle.load(f)
        
    with open(PC.TFIDF_PATH, "rb") as f:
        tfidf = pickle.load(f)

    # parse the ingredients using my ingredient_parser 
    try: 
        ingredients_parsed = ingredient_parser(ingredients)
    except:
        ingredients_parsed = ingredient_parser([ingredients])
    
    # use our pretrained tfidf model to encode our input ingredients
    ingredients_tfidf = tfidf.transform([ingredients_parsed])

    # calculate cosine similarity between actual recipe ingreds and test ingreds
    cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)

    # Filter top N recommendations 
    recommendations = get_recommendations(N, scores)
    return recommendations

if __name__ == "__main__":
    # test ingredients
    test_ingredients = "1 c. firmly packed brown sugar, 1/2 c. evaporated milk, 1/2 tsp. vanilla, 1/2 c. broken nuts (pecans), 2 Tbsp. butter or margarine, 3 1/2 c. bite size shredded rice biscuits"
    recs = RecSys(test_ingredients)
    print(recs)
    # print(recs.score)