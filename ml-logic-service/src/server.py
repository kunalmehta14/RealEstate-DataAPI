from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from redis_vector_search import process_request
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
from llama_cpp.llama import Llama, LlamaGrammar
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

#Global Logging Configuration
logging.basicConfig(filename='/var/log/server.log', encoding='utf-8')

class Server(BaseHTTPRequestHandler):
  # LAMA LANGCHAIN MODEL LOAD
  MODEL_PATH = r'./llms/2b_it_v2.gguf'
  callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
  load_llama_model = Llama(model_path=MODEL_PATH,
                            max_tokens=2000,
                            top_p=1,
                            callback_manager=callback_manager,
                            verbose=True)

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
        
  def do_HEAD(self):
    self._set_headers()

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
        # Process the user's query and receive AI response
        ai_response = process_request(message, llama_model=self.load_llama_model)
        log['Level'] = 'Info'
        log['Message'] = f'''Processed the user query {message}
                             successfully returned.'''
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