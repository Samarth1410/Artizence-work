from gevent import 
monkey 
 monkey.patch_all() # This is required for all external web requests to work properly. 
  
 from flask import Flask, request, Response, jsonify 
 from pydub import AudioSegment 
 import os, gtts, random, uuid, wavio, json, numpy as np 
  
 import nuva_ai as ai 
 from ext.rule_documenter import RuleDocumenter 
  
  
 app = Flask(_name_) 
 rule_documenter = RuleDocumenter() 
  
  
 @app.route("/health") # health check endpoint. Might be used while deploying. 
 @app.route("/") # This server is not meant for visitors, so let's just display "OK" here. 
 def _empty() -> str: 
     return "OK" 
  
 @app.route("/endpoints") # a list of endpoints available 
 def _endpoints() -> Response: 
     if app.debug == True: print(rule_documenter.get_rules()) # if debug mode is on, log the data. 
     return jsonify(rule_documenter.get_rules()) 
  
  
 @app.route("/audio", methods=["GET", "POST"]) 
 @rule_documenter.define( 
     path="/audio", 
     request={ 
         "type": "json", 
         "fields": { 
             "data": "The data to be processed. Should be an array for analog, plain bytes for digital.", 
             "type": "The type of data [\"digital\" or \"analog\"]." 
         } 
     }, 
     response={ 
         "type": "file", 
         "data": "The wav file for the response message." # data can be a dict if type is json, and can describe multiple fields 
     }, 
     methods=["POST"] # only accept POST requests. Although GET is also accepted, it is just added to flask to return an 
 ) 
 def audio() -> Response: 
     """ 
     This accepts a wav file from the client in the form of analog signals or a wav upload  
     and uses AI to produce a response message. This response message is then converted   
     into a wav file and sent back to the client. 
     """ 
     if(request.method == "POST"): 
         response = "" 
         statusCode = 200 
         if True: 
         #try: 
             try: 
                 #f = request.get_json(force=True) 
                 data = request.files['data'] 
                 data_type = request.files["type"] 
              
             except: 
                 statusCode = 400 
                 raise Exception("No JSON data") 
  
             # create a file and write all given data to it 
             file = str(f"uploads/{uuid.uuid4()}.wav") 
  
             # if data or type is not a property of the request, it will throw an error. 
             if data is None: 
                 statusCode = 400 
                 raise Exception("No data given.") 
             if data_type is None: 
                 statusCode = 400 
                 raise Exception("No type given.") 
  
             print('data_type',data_type) 
             if data_type == "analog": 
                 # convert the data to wav 
                 """ 
                 try: 
                     data = json.loads(data) 
                 except: 
                     statusCode = 400 # the data is not an array which is expected 
                     raise Exception("Invalid data given.")""" 
                 wavio.write(file, np.ndarray(data), 44100)  
  
             elif data_type == "digital": 
                 # write the data to a file 
                 with open(file, "wb") as f: 
                     f.write(data) 
              
             else: 
                 print('wav or other') 
                 #statusCode = 400 
                 #raise Exception("Invalid data type.") 
  
             try: 
                 response = get_response(file) 
             except: 
                 response = 'error in input data' 
         #except: 
         else: 
             #if statusCode == 200: statusCode = 500  
             # this means that the status code was not changed, thus would be a server error probably. 
             response = "An error occurred. Please try again." 
           
             
         # delete the temporary file 
         if os.path.exists(file): os.remove(file) 
         # return audio response. 
         #return to_audio_response(response, status=statusCode) 
         return to_audio_response(response) 
     else: 
         return to_audio_response("Client is misconfigured... Cannot perform operation.") 
  
  






















  
 @app.route("/text", methods=["GET", "POST"]) 
 @rule_documenter.define( 
     path="/text", 
     request={ 
         "type": "json", 
         "fields": { 
             "text": "The text to generate a response for." 
         } 
     }, 
     response={ 
         "type": "json", 
         "data": { 
             "text": "The response message." 
         } 
     }, 
     methods=["GET", "POST"] 
 ) 
 def text() -> Response: 
     """ 
     This accepts a message from the client and uses AI to produce a response message.  
     This response message is then sent back to the client. 
     """ 
     statusCode = 200 
     try: 
         try: 
             f = request.get_json(force=True) 
             print(f) 
         except: 
             statusCode = 400 
             raise Exception("No JSON data") 
  
         if f.get("text") is None: 
             statusCode = 400 
             raise Exception("No text given.") 
  
         response = ai.get_response(f["text"]) 
     except: 
         if statusCode == 200: statusCode = 500  
         # this means that the status code was not changed, thus would be a server error probably. 
         response = "An error occurred. Please try again." 
     return Response(response, status=statusCode) 
