from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi, json
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from redis_vector_search import redis_search
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
logging.basicConfig(filename='/var/log/server.log', encoding='utf-8')

class Server(BaseHTTPRequestHandler):
  # Vector embedding opensource model, accessed using huggingface
  # https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
  embedding_model_path = "sentence-transformers/all-MiniLM-L12-v2"
  embedding_model = SentenceTransformer(embedding_model_path)

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
        
  def do_HEAD(self):
    self._set_headers()

  def goggleChatResponse(self, message):
    log = dict()
    log['Function'] = 'goggleChatResponse()'
    try:
      prompt_instructions = open('prompt_instructions')
      genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
      # Create the model
      generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
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
  
  def do_POST(self):
    log = dict()
    if self.path == '/vector-search':
      log['Function'] = 'do_POST()'
      log['Endpoint'] = 'vector-search'
      try:
        form = cgi.FieldStorage(
          fp=self.rfile,
          headers=self.headers,
          environ={'REQUEST_METHOD': 'POST',
                  'CONTENT_TYPE': self.headers['Content-Type'],
                  }
        )
        message = form.getvalue("chat")
        # send the message back
        source_information = redis_search(message, self.embedding_model)
        # Get the formated results
        formated_results = []
        for idx in range(1, len(source_information)):
          if idx % 2 == 0:
            formated_results.append(source_information[idx][1])
        # updated_result = json.dumps(formated_results)
        combined_information = f""" User Query:
                            {message}

                            Search Results, formatted in array:
                            {formated_results}"""
        ai_response = self.goggleChatResponse(combined_information)
        log['Level'] = 'Info'
        log['Message'] = f'''Processed the user query {message}
                           successfully returned following 
                           number of results: {len(formated_results)}.'''
        log['Status'] = '200'
        logging.info(log)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(ai_response.encode('utf-8'))
      except Exception as e:
        log['Level'] = 'Error'
        log['Message'] = f'''Could not process the request
                         due to the following reasons: {e}'''
        log['Status'] = '404'
        logging.error(log)
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 - Not Found')
        
def mllogic_http_server_run(server_class=HTTPServer, handler_class=Server, port=8010):
  log = dict()
  log['Function'] = ' mllogic_http_server_run()'
  try:
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    log['Level'] = 'Info'
    log['Message'] = f"Starting httpd on port: {port}"
    logging.info(log)
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()
  except Exception as e:
    log['Level'] = 'Error'
    log['Message'] = f'''Could not process the request
                      due to the following reasons: {e}'''
    logging.error(log)

mllogic_http_server_run()