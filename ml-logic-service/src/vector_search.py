# Old function, replaced with redis_vectory_search.

from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import re
import numpy as np

def generate_description(df, row):
    # collective_info = ''
    # for col in df.columns:
    #     collective_info = collective_info + f" {col}: {row[col]}"
    # return collective_info
  description = f""" This property listing is located in the city {row['CityName']} in Canada, 
               which has population of {row['PopulationLatest']} and has {row['Beds']} bedrooms and 
               {row['Baths']} bathrooms. It is a {row['ListingType']} with total area of 
               {row['Area']}. It has {row['Schools']} schools, {row['Colleges']} colleges, {row['Universities']} universities,
               {row['Ameneties']} and {row['Airbnbs']} AirBNBs nearby. The property is listed for ${row['Price']}.
               The following property falls under the price categorization of {row['PriceCategorization']}."""
  return description

embedding_model_path = "sentence-transformers/all-MiniLM-L12-v2"
embedding_model = SentenceTransformer(embedding_model_path)

def get_embedding(text):
  if not text.strip():
    print("Attempted to get embedding for empty text.")
    return []
  embedding = embedding_model.encode(text)
  return embedding.tolist()

def get_search_result(query, df, details_col, embedding_col):
  exact_matches = []
  if '"' in query or "'" in query:
    exact_matches = re.findall(r'"(.*?)"', query)
  query_embedding = get_embedding(query)
  df["similarities"] = df[embedding_col].apply(lambda x: util.pytorch_cos_sim(x, query_embedding))
  values = df.sort_values("similarities")
  threshold = 0.40
  similar_pairs = []
  for index, row in values.iterrows():
    score = np.argwhere(row['similarities'] > threshold)
    if score.numel() > 0:
      if len(exact_matches) == 0:
        similar_pairs.append(f'Listing Information: {row[details_col]}')
      else:
        for exact_match in exact_matches:
          if exact_match in row[details_col]:
            similar_pairs.append(f'Listing Information: {row[details_col]}')          
  return similar_pairs

def embedded_data(df):
    embeddingcol = "embedding"
    detailscol = "Description"
    df[detailscol] = df.apply(lambda row: generate_description(df, row), axis=1)
    df[embeddingcol] = df[detailscol].apply(get_embedding)
    return df