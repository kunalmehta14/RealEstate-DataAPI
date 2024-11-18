import os, logging
import mysql.connector
from sentence_transformers import SentenceTransformer
import json, ast
import redis
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
logging.basicConfig(filename='/var/log/application.log', encoding='utf-8')

def get_embedding(text, embedding_model_path):
  embedding_model = SentenceTransformer(embedding_model_path)
  if not text.strip():
    log = dict()
    log['Level'] = 'Error'
    log['Function'] = 'get_embedding()'
    log['Message'] = f'''Message: Attempted to get 
                       embedding for empty text: {text}'''
    logging.error(log)
    return []
  embedding = embedding_model.encode(text)
  return embedding.tolist()

def aggregate_data():
  log = dict()
  log['Function'] = 'aggregate_data()'
  log['Level'] = 'Info'
  try:
    # Establish Connection To The MySQL Server
    conn = mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DATABASE"),
        port = os.getenv("MYSQL_PORT"),
        buffered = True)
    cursor = conn.cursor(buffered=True , dictionary=True)
    # Get just the listing Ids to make the query process more efficient
    cursor.execute('SELECT Id FROM RealEstateListings ORDER BY Id DESC')
    listing_ids = cursor.fetchall()
    # Load the embedding model for vector creation process
    embedding_model_path = "sentence-transformers/all-MiniLM-L12-v2"
    # Establish Redis Connection
    redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), 
                                     port=os.getenv("REDIS_PORT"), db=0, 
                                     password=os.getenv("REDIS_PASSWORD"))
    
    # Loop Over the Listing Ids
    for id in listing_ids:
      try:
        log['Message'] = f'''Checking the redis 
                           enteries for entryid: {id['Id']}'''
        logging.info(log)
        redis_key = f"item:{id['Id']}"
        redis_entry_list = redis_client.execute_command("JSON.GET", redis_key)
        if redis_entry_list == None:
          log['Message'] = f"""Entry Id: {id['Id']} doesn't existing in the redis database, 
                             aggregating information and generating vector embeddings."""
          logging.info(log)
          # SQL Query is too large, therefor Query is read using the file 'GetListingData.sql'
          sql_query_file = open('GetListingData.sql')
          sql_query = sql_query_file.read().replace('??', f"{id['Id']}")
          cursor.execute(sql_query,) 
          list_detail = cursor._fetch_row()
          ###################################
          ## Generate Filtered Description ##
          ###################################
          # Base Description
          base_description =  f"""Property located at {list_detail['AddressStreet']} in {list_detail['CityName']} - {list_detail['CityType']} in division of {list_detail['Division']} in Ontario, offers {list_detail['Beds']} bedrooms and {list_detail['Baths']} bathrooms. The listing, listed under {list_detail['ListingType']} on {list_detail['ListingDate']}.\n"""
          price_details = f"""Price history: Original price: CAD {list_detail['OrignalPrice']}, Current price: CAD {list_detail['CurrentPrice']} The property is {list_detail['DaysOnTheMarket']}.\n"""
          # Area description
          area_description = None
          if list_detail['Area'] != None:
            area_description = f"The property spans {list_detail['Area']} square feet.\n"
          # Add ameneties details
          ameneties_details = None
          if list_detail['Ameneties'] != None:
            ameneties_details = f"This property is in proximity to the {list_detail['NumberOfAmeneties']} amenties:\n"
            ameneties = list_detail['Ameneties'].split('| ')
            for i in range(len(ameneties)):
              info = f'{i}. {ameneties[i]}\n'
              ameneties_details = ameneties_details + info
          # Add school details
          school_details = None
          if list_detail['Schools'] != None:
            school_details = f"This property is in proximity to following schools:\n"
            schools = list_detail['Schools'].split(', ')
            for i in range(len(schools)):
              info = f'{i}. {schools[i]}\n'
              school_details = school_details + info
          # Add school details
          colleges_details = None
          if list_detail['Colleges'] != None:
            colleges_details = f"This property is in proximity to following colleges:\n"
            colleges = list_detail['Colleges'].split(', ')
            for i in range(len(colleges)):
              info = f'{i}. {colleges[i]}\n'
              colleges_details = colleges_details + info
          # Add university details
          universities_details = None
          if list_detail['Universities'] != None:
            universities_details = f"This property is in proximity to following universities:\n {list_detail['Universities']}\n"
          # Airbnbs nearby
          airbnbs_description = None
          if list_detail['NumberOfAirbnbs'] != 0:
            airbnbs_description = f"The neighborhood has {list_detail['NumberOfAirbnbs']} Airbnbs with an average price of CAD {list_detail['AirbnbsAvergePrice']}.\n"
          # Walkscore
          walkscore_description = None
          if list_detail['WalkScore'] != None:
            walkscore_description = f"This property has a Walk Score of {list_detail['WalkScore']}\n"
          # Transit
          transitscore_description = None
          if list_detail['WalkScore'] != None:
            transitscore_description = f"Transit score {list_detail['TransitScore']}\n"
          # Other details about property
          other_details = f"Property details:\nBasement: {list_detail['Basement']}\nTax amount: CAD {list_detail['TaxAmount']}\nFireplace: {list_detail['Fireplace']}\nGarage: {list_detail['Garage']}\nHeating: {list_detail['Heating']}\nSewer: {list_detail['Sewer']}"
          # Addiitonal Description
          additional_description = None
          if list_detail['Description'] != None:
            additional_description = f"Additional Description provided by the author of the listing: {list_detail['Description']}\n"
          # Final Generated description
          generated_description = ''
          generated_description_vars = [base_description, price_details, area_description, ameneties_details,
                                        school_details, colleges_details, universities_details, airbnbs_description,
                                        walkscore_description, transitscore_description, other_details,
                                        additional_description]
          for var in generated_description_vars:
            if var != None:
              generated_description = generated_description + var
          # Generate Embedding Data Values
          vec_emb_val = get_embedding(generated_description, embedding_model_path)
          endpoint = f"realestatelistings/{id['Id']}/"
          data = {
            "id": id['Id'],
            "item_description": generated_description,
            "endpoint": endpoint,
            "vector_embeddings": vec_emb_val
          }
          redis_key = f"item:{id['Id']}"
          response = redis_client.execute_command("JSON.SET", redis_key, '$', json.dumps(data))
          log['Message'] = f'''The values for {redis_key} insert 
                             process response: response-{response}'''
          logging.info(log)
      except Exception as e:
        log['Level'] = 'Error'
        log['Message'] = f'''Error received when trying to execute 
                          the aggregate_data() function
                          for the entry id: {id['Id']}: {e}'''
        logging.info(log)
        pass
  except Exception as e:
    log['Level'] = 'Error'
    log['Message'] = f'''Error received when trying to execute 
                      the aggregate_data() function: {e}'''
    logging.error(log)


aggregate_data()