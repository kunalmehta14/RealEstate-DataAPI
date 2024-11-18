import os, logging
import numpy as np
import redis
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Global Logging Configuration
logging.basicConfig(filename='/var/log/application.log', encoding='utf-8', level=logging.DEBUG)

def get_embedding(text, embedding_model):
  if not text.strip():
    print("Attempted to get embedding for empty text.")
    return []
  embedding = embedding_model.encode(text)
  return embedding.astype(np.float64)

def redis_search(query, embedding_model):
  log = dict()
  log['Function'] = 'redis_search()'
  try:
    log['Level'] = 'Info'
    log['Message'] = f'User query received: {query}'
    logging.info(log)
    query_emb = get_embedding(query, embedding_model)
    query_vector_blob = np.array(query_emb).tobytes()
    redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), 
                                      port=os.getenv("REDIS_PORT"), db=0, 
                                      password=os.getenv("REDIS_PASSWORD"))
    results = redis_client.execute_command(
      "FT.SEARCH", "searchIdx", "*=>[KNN 10 @vector $query_vector]",
      "SORTBY", "__vector_score", "ASC", 
      "RETURN", "1", "item_description",
      "DIALECT", "2", 
      "PARAMS", "2", "query_vector", query_vector_blob
    )
    return results
  except Exception as e:
    log['Level'] = 'Error'
    log['Message'] = f'Error processing search query using redis search: {e}'
    logging.error(log)