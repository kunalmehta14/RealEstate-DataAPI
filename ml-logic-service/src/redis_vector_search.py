import os, logging
import numpy as np
import redis
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
import google.generativeai as genai
# Import Spacy for processing search queries
import spacy
# Load the English NLP model
nlp = spacy.load("en_core_web_sm")
# Temporary Change
from sentence_transformers import SentenceTransformer
# Global Logging Configuration
logging.basicConfig(filename='/var/log/application.log', encoding='utf-8', level=logging.DEBUG)


# Vector embedding opensource model, accessed using huggingface
# https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
embedding_model_path = "sentence-transformers/all-MiniLM-L12-v2"
embedding_model = SentenceTransformer(embedding_model_path)

def get_embedding(text):
  if not text.strip():
    print("Attempted to get embedding for empty text.")
    return []
  embedding = embedding_model.encode(text)
  return embedding.astype(np.float64)

def redis_search_query_creator(text):
  # Process the text
  doc = nlp(text)
  # Combine text into search query
  search_text = ''
  temp = []
  results = []
  proper_nouns = []
  for token in doc:
    # Combine sequences of numbers and proper nouns/adjectives
    if token.pos_ in ["PROPN", "NUM", "ADJ", "NOUN"]:
      results.append(token.text)
    # To Create Search Boost Query
    if token.pos_ in ["PROPN"]:
      proper_nouns.append(token.text)
  # Loop through the keywords to create a redis search query
  for i in range(len(results)):
    if i == 0 and len(results) == 1:
      search_text = search_text + f'(@item_description:{results[i]}*)'
    elif i == 0 and len(results) > 1:
      search_text = search_text + f'(@item_description:{results[i]}* |' 
    elif i == (len(results) - 1):
      search_text = search_text + f' @item_description:{results[i]}*' + ')'
    else:
      search_text = search_text + f' @item_description:{results[i]}* |'
  # Create Search Boost Query
  search_boost_pnoun = ''
  for i in range(len(proper_nouns)):
    if i == 0 and len(proper_nouns) == 1:
      search_boost_pnoun = search_boost_pnoun + f'(@item_description:{proper_nouns[i]})' + '=>{ $weight: 5.0; }'
    elif i == 0 and len(proper_nouns) > 1:
      search_boost_pnoun = search_boost_pnoun + f'(@item_description:{proper_nouns[i]} |' 
    elif i == (len(proper_nouns) - 1):
      search_boost_pnoun = search_boost_pnoun + f' {proper_nouns[i]}' + ')' + '=>{ $weight: 5.0; }'
    else:
      search_boost_pnoun = search_boost_pnoun + f' {proper_nouns[i]} |'
  if search_boost_pnoun != '':
    search_text = '(' + search_text + ' | ' + search_boost_pnoun + ')'
    return search_text
  else:
    return search_text

def redis_search(query):
  log = dict()
  log['Function'] = 'redis_search()'
  try:
    log['Level'] = 'Info'
    log['Message'] = f'User query received: {query}'
    extracted_keywords = redis_search_query_creator(query)
    logging.info(log)
    query_emb = get_embedding(query)
    query_vector_blob = np.array(query_emb).tobytes()
    redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), 
                                      port=os.getenv("REDIS_PORT"), db=0, 
                                      password=os.getenv("REDIS_PASSWORD"), 
                                      socket_timeout=10000)
    search = f"{extracted_keywords}=>[KNN 20 @vector $query_vector]"
    print(search)
    results = redis_client.execute_command(
      "FT.SEARCH", "searchIdx", search,
      "RETURN", "1", "item_description",
      "PARAMS", "2", "query_vector", query_vector_blob,
      "DIALECT", "2"
    )
    return results
  except Exception as e:
    print(e)
    log['Level'] = 'Error'
    log['Message'] = f'Error processing search query using redis search: {e}'
    logging.error(log)

def goggleChatResponse(message):
  log = dict()
  log['Function'] = 'goggleChatResponse()'
  try:
    prompt_instructions = open('prompt_instructions')
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 1,
      "max_output_tokens": 8192
    }
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
      system_instruction= prompt_instructions,
    )
    chat_session = model.start_chat(
      history=[
      ]
    )
    response = chat_session.send_message(message)
    return response.text
  except Exception as e:
    log['Level'] = 'Error'
    log['Message'] = f'''Could not process the request
                        due to the following reasons: {e}'''
    logging.error(log)

def process_request(message, llama_model):
  model_prompt = f"""User Query: {message}
                    Analyze the "User query" and respond with one word from these options:
                    RealEstate: Property listings, buying/selling homes, rentals.
                    MortgageRates: Interest rates, loan terms, financing.
                    Other: Anything else.
                  """
  process_query = llama_model(model_prompt)
  llama_proc_res = process_query['choices'][0]['text']
  if 'RealEstate' in llama_proc_res:
    source_information = redis_search(message)
    # Get the formated results
    formated_results = []
    for idx in range(1, len(source_information)):
      if idx % 2 == 0:
        formated_results.append(source_information[idx][1])
    # Generate AI Prompt
    combined_information = f""" User Query:
                        {message}

                        Search Results, formatted in array:
                        {formated_results}"""
    ai_response = goggleChatResponse(combined_information)
    return ai_response