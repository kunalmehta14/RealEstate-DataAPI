from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi, json
import pandas as pd
import google.generativeai as genai
from vector_search import get_search_result, embedded_data
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
class Server(BaseHTTPRequestHandler):
  user_query = {}
  vector_df = None
  
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
        
  def do_HEAD(self):
    self._set_headers()

  def goggleChatResponse(self, message):
    genai.configure(api_key=os.getenv("GOOGLE_API"))
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
      system_instruction=""" You're an experienced real estate agent.
                          Please analyze the user's query and the provided search results.
                          Verify the results match the user query and provide summarized insights
                          to each search result. Use the information from the search results to 
                          generate a structured and comprehensive response to the user's query.""",
    )
    chat_session = model.start_chat(
      history=[
      ]
    )
    response = chat_session.send_message(message)
    return response.text    
  
  def do_POST(self):
    if self.path == '/vector-search':
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
        source_information = get_search_result(message, Server.vector_df, 
                                              details_col='Description', 
                                              embedding_col='embedding')
        updated_result = json.dumps(source_information)
        print(updated_result)
        combined_information = f""" User Query:
                            {message}

                            Search Results, formatted in array:
                            {updated_result}"""
        ai_response = self.goggleChatResponse(combined_information)
        print(ai_response)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(ai_response.encode('utf-8'))
      except:
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 - Not Found')
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
  df = pd.read_csv("RealEstateData.csv")
  # Gather collective information about each column
  col_val = []
  for col in df.columns:
    col_val.append(col)
  print(df.shape[0])
  updated_df = embedded_data(df)
  Server.vector_df = updated_df
  print(f"DataFrame loaded with {len(Server.vector_df)} rows.")
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)

  print('Starting httpd on port %d...' % port)
  httpd.serve_forever()
    
run()